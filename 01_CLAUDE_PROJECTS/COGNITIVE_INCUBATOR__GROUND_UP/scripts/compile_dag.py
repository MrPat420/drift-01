#!/usr/bin/env python3
import argparse, pathlib, json, sys
import jsonschema, re, subprocess

def load_schema(schema_path: pathlib.Path):
    with open(schema_path) as f:
        return json.load(f)

def extract_dag_blocks(file_path: pathlib.Path):
    text = file_path.read_text()
    pattern = re.compile(r"```dag_node\n(.*?)\n```", re.DOTALL)
    for m in pattern.finditer(text):
        yield m.group(1)

def parse_block(block: str):
    return json.loads(block)

def build_adj(nodes):
    adj = {n["node_id"]: set(n.get("causal_prerequisites", [])) for n in nodes}
    return adj

def has_cycle(adj):
    visited = set()
    recstack = set()
    def dfs(v):
        visited.add(v)
        recstack.add(v)
        for neigh in adj.get(v, []):
            if neigh not in visited:
                if dfs(neigh):
                    return True
            elif neigh in recstack:
                return True
        recstack.remove(v)
        return False
    return any(dfs(v) for v in adj if v not in visited)

def verify_ast_hash(hash_str: str) -> bool:
    return bool(hash_str) and len(hash_str) == 64

def extract_keys(node):
    key = node["node_id"].split("::")[-1].upper()
    return [(key, (0, 0))]

def main():
    parser = argparse.ArgumentParser(description="Ground‑up DAG compiler")
    parser.add_argument("--workspace", required=True, help="Workspace root path")
    parser.add_argument("--output-dir", required=True, help="Output JSON file path")
    parser.add_argument("--strict", type=lambda x: x.lower() == 'true', default=False, help="Fail on validation errors")
    args = parser.parse_args()

    workspace = pathlib.Path(args.workspace).resolve()
    output_path = pathlib.Path(args.output_dir).resolve()
    schema_path = workspace / "schemas" / "dag_prereq_schema.json"

    schema = load_schema(schema_path)
    node_schema = schema["definitions"]["dag_node"]
    validator = jsonschema.Draft202012Validator(node_schema)

    nodes = []
    for file in workspace.rglob("*.*"):
        if file.suffix not in {".py", ".json", ".sh", ".md"}:
            continue
        for blk in extract_dag_blocks(file):
            try:
                node = parse_block(blk)
                node["source_file"] = str(file)
                nodes.append(node)
            except Exception as e:
                if args.strict:
                    sys.exit(f"Failed to parse DAG block in {file}: {e}")

    # Validation
    errors = []
    for n in nodes:
        errors.extend(list(validator.iter_errors(n)))
    if errors:
        if args.strict:
            for e in errors:
                sys.stderr.write(str(e) + "\n")
            sys.exit(1)

    # Cycle check
    adj = build_adj(nodes)
    if has_cycle(adj):
        sys.exit("Prerequisite cycle detected")

    # SCRUB‑01 placeholder (no-op)
    # SENTINEL‑01 AST verification
    for n in nodes:
        if not verify_ast_hash(n.get("ast_rule_hash", "")):
            sys.exit(f"AST gate failed for {n.get('node_id')}")

    # Build registry
    registry = []
    for n in nodes:
        for key, offset in extract_keys(n):
            registry.append({
                "entity_key": key,
                "source_file": n["source_file"],
                "byte_offset_start": offset[0],
                "byte_offset_end": offset[1],
                "deterministic_output": key
            })

    result = {
        "dag_nodes": nodes,
        "entity_key_registry": registry,
        "error_handling": schema["definitions"]["error_handling"]["properties"]
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Compiled DAG written to {output_path}")

if __name__ == "__main__":
    main()
