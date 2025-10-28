import json
from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import Any

router = APIRouter()

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

@router.get("/laws", tags=["laws"])
def get_law_list() -> list[dict[str, Any]]:
    """
    Returns the content of mock_law_list.json.
    Matches spec: GET /laws
    """
    mock_file_path = PROJECT_ROOT / "mock_law_list.json"
    with open(mock_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.get("/law/{law_id}", tags=["laws"])
def get_law_detail(law_id: str, promulgationNo: str | None = None) -> dict[str, Any]:
    """
    Returns the content of mock_law_detail_001322_02889.json
    if the law_id matches.
    Matches spec: GET /law/{법령ID}?promulgationNo={공포번호}
    """

    laws = [] 
    mock_file_path = PROJECT_ROOT / "mock_law_detail_001322_02889.json"
    with open(mock_file_path, 'r', encoding='utf-8') as f:
        laws.append(json.load(f))

    # Get the ID from the mock file: data['법령']['기본정보']['법령ID']
    
    # mock_law_id = data.get("법령", {}).get("기본정보", {}).get("법령ID")

    # 법령이 여러개 있을 때를 가정
    for law in laws:
        _law_id = law.get("법령", {}).get("기본정보", {}).get("법령ID")
        
        if _law_id == law_id:
            if promulgationNo:
                _promulgation_no = law.get("법령", {}).get("기본정보", {}).get("공포번호")
                if promulgationNo == _promulgation_no:
                    return law
                else:
                    continue
            return law
        
    raise HTTPException(status_code=404, detail="Law not found")
