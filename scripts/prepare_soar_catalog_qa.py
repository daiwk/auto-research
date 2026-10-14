"""Public tool-catalog KB first, then tool-group-disjoint TRAINING attribute QA.

Only the authorized fixed catalog CSV is opened. Neither train_pairs.csv nor
eval_real_test.jsonl is an input. QA gold lives in scorer files, never KB fields.
This derived training diagnostic is not RATED or SOAR's official benchmark.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

PUBLIC_ID="Elliotes/EcoAgent"
REVISION="bc5db40a20b254c5249401d2220ea71b06c86a5c"
CATALOG_SHA="1b388d317aeb1004c266eb65ff64a4864e7907412a2fbfb4667c492a871e8d8e"
FILENAME="tools_clean_with_reliability.csv"
SOURCE_URL=f"https://github.com/Elliotes/EcoAgent/blob/{REVISION}/data/processed/{FILENAME}"
QA_SOURCE_ID="Elliotes/EcoAgent#derived-tool-document-attribute-training-QA-v1"


def encode_rows(rows):
    return "".join(json.dumps(row,ensure_ascii=False)+"\n" for row in rows).encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def independent_documents(catalog, *, max_chars=900):
    """Uses original public descriptive fields only, never QA selection or labels."""
    if max_chars<100:
        raise ValueError("use an explicit positive document character cap")
    documents=[]
    for row in catalog:
        text=("Tool name: "+row["name"]+"\nCatalog UID: "+row["uid"]+
              "\nSource collection: "+row["source"]+"\nDocumentation URL: "+row["url"]+
              "\nTags: "+row["tags"]+"\nDescription: "+row["description"])
        for index,begin in enumerate(range(0,len(text),max_chars)):
            piece=text[begin:begin+max_chars]
            if not piece.strip():
                continue
            document={"id":row["uid"]+":"+str(index),"tool_group":row["uid"],"title":row["name"],
                      "text":piece,"source_url":SOURCE_URL,"source_character_start":begin,
                      "source_character_end":begin+len(piece)}
            document["source_row_sha256"]=digest(json.dumps(document,sort_keys=True,ensure_ascii=False).encode())
            documents.append(document)
    return documents


def partition_questions(catalog, *, train_tools=8, validation_tools=4):
    if min(train_tools,validation_tools)<1:
        raise ValueError("positive disjoint tool-group budgets required")
    names=Counter((row["name"],row["source"]) for row in catalog)
    selected={"train":[],"validation":[]}
    groups={"train":[],"validation":[]}
    for row in catalog:
        group=row["uid"]
        key=(row["name"],row["source"])
        if names[key]!=1 or not all(row[k].strip() for k in ("name","uid","source","url")):
            continue
        # Bound question/answer serialization before model use; no model outcomes are inspected.
        if len(row["name"])+len(row["source"])+len(row["url"])+len(group)>650:
            continue
        hash_value=hashlib.sha256(("soar-tool-group-v1|"+group).encode()).digest()
        split="validation" if int.from_bytes(hash_value[:8],"big")/2**64<0.2 else "train"
        needed=train_tools if split=="train" else validation_tools
        if len(selected[split])>=needed:
            continue
        attribute="catalog UID" if hash_value[-1]%2==0 else "documentation URL"
        answer=group if attribute=="catalog UID" else row["url"]
        question=("Use the search tool to retrieve the public catalogue entry before answering. For the tool named "+
                  json.dumps(row["name"],ensure_ascii=False)+" in the source collection "+
                  json.dumps(row["source"],ensure_ascii=False)+", what is its "+attribute+
                  "? Return only that exact attribute value in your answer and declare its information source.")
        selected[split].append({"question":question,"answer":answer,"tool_group":group,
                                "attribute":attribute,"source_url":SOURCE_URL})
        groups[split].append(group)
        if len(selected["train"])==train_tools and len(selected["validation"])==validation_tools:
            break
    if len(selected["train"])!=train_tools or len(selected["validation"])!=validation_tools:
        raise ValueError("insufficient genuine catalogue tool groups for requested split")
    if set(groups["train"]) & set(groups["validation"]):
        raise ValueError("tool-group overlap")
    return selected,groups


def write_json(path,value):
    with path.open("x") as stream:
        stream.write(json.dumps(value,ensure_ascii=False,indent=2)+"\n")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--train-tools",type=int,default=8)
    parser.add_argument("--validation-tools",type=int,default=4)
    parser.add_argument("--max-chars",type=int,default=900)
    args=parser.parse_args()
    if args.output.exists():
        raise FileExistsError("prepared sources are immutable; use a fresh output directory")
    raw=args.catalog.read_bytes()
    if digest(raw)!=CATALOG_SHA:
        raise ValueError("fixed official public catalogue bytes mismatch")
    previous=csv.field_size_limit()
    try:
        csv.field_size_limit(16*1024*1024)
        with args.catalog.open(newline="",encoding="utf-8-sig") as stream:
            reader=csv.DictReader(stream)
            if not {"uid","name","description","source","url","tags"}.issubset(reader.fieldnames or []):
                raise ValueError("required original catalogue fields are absent")
            catalog=list(reader)
    finally:
        csv.field_size_limit(previous)
    if len({row["uid"] for row in catalog})!=len(catalog):
        raise ValueError("public catalogue tool identifiers are not unique")
    args.output.mkdir(parents=True,exist_ok=False)
    kb=args.output/"kb"
    kb.mkdir()
    # Stage 1: seal the complete independent KB BEFORE selecting any QA tool groups.
    documents=independent_documents(catalog,max_chars=args.max_chars)
    document_bytes=encode_rows(documents)
    (kb/"documents.jsonl").write_bytes(document_bytes)
    generator_sha=digest(Path(__file__).read_bytes())
    write_json(kb/"provenance.json",{"kind":"dataset","public_id":PUBLIC_ID,"revision":REVISION,
               "split":"train","split_semantics":"user-authorized derived training KB; upstream catalogue has no official QA split",
               "rows":len(documents),"files":{"documents.jsonl":digest(document_bytes)},
               "upstream_file":FILENAME,"upstream_sha256":CATALOG_SHA,"source_url":SOURCE_URL,
               "generator_sha256":generator_sha,"full_catalog_tools":len(catalog),
               "transformation":"all original tool name/UID/source/URL/tags/description; contiguous character chunks",
               "max_document_characters":args.max_chars,"qa_selection_input_read":False,
               "train_pairs_input_read":False,"official_test_opened":False,
               "excluded_fields":"reliability/completeness/quality scores and all training/test QA labels",
               "diagnostic_only":True,"not_rated_or_soar_official_benchmark":True})
    # Stage 2: training diagnostic questions, partitioned by original tool UID.
    selected,groups=partition_questions(catalog,train_tools=args.train_tools,validation_tools=args.validation_tools)
    source_bytes=encode_rows(selected["train"]+selected["validation"])
    (args.output/"source-training-qa.jsonl").write_bytes(source_bytes)
    partitions={}
    for split,rows in selected.items():
        content=encode_rows(rows)
        (args.output/(split+".jsonl")).write_bytes(content)
        partitions[split]=digest(content)
    write_json(args.output/"split.json",{"source_id":QA_SOURCE_ID,"source_revision":REVISION,
               "source_sha256":digest(source_bytes),"source_split":"train","test_opened":False,
               "source_split_semantics":"locally generated training-QA pool, NOT an EcoAgent official train split",
               "upstream_source_scope":"independent public catalog only; no train_pairs or eval_real_test",
               "upstream_public_id":PUBLIC_ID,"upstream_file":FILENAME,"upstream_sha256":CATALOG_SHA,
               "generator_sha256":generator_sha,"independent_kb_sha256":digest(document_bytes),
               "partition":"tool UID sha256(soar-tool-group-v1|UID) unsigned 64-bit prefix <0.2 validation; original-order bounded prefixes",
               "counts":{k:len(v) for k,v in selected.items()},"partition_sha256":partitions,
               "tool_groups":groups,"tool_groups_disjoint":True,"shared_complete_kb":True,
               "formal_generalization_claim":False,"diagnostic_only":True})
    print(json.dumps({"catalog_tools":len(catalog),"kb_documents":len(documents),"kb_bytes":len(document_bytes),
                      "train_qa":len(selected["train"]),"validation_qa":len(selected["validation"]),
                      "kb_sha256":digest(document_bytes),"partition_sha256":partitions,
                      "generator_sha256":generator_sha,"official_test_opened":False},ensure_ascii=False))


if __name__=="__main__":
    main()
