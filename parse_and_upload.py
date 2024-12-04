import json
import requests
import sys
import os

def parse_txt_to_json(txt_file):
    data = []
    current_item = {}

    with open(txt_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        # 빈 줄이나 불필요한 헤더/푸터 무시
        if not line or line.startswith("#") or line.startswith("점검일") or line.startswith("="):
            continue

        # ID 및 카테고리 정보 파싱
        if line.startswith("▶ U-"):
            if current_item:  # 이전 항목 저장
                data.append(current_item)
            current_item = {}

            # ID 및 중요도 추출
            id_and_category = line.split("|")
            current_item["id"] = id_and_category[0].split("▶")[-1].strip()
            current_item["importance"] = id_and_category[1].strip("()").strip()

            # 카테고리 및 점검 항목 처리
            if len(id_and_category) > 2:
                category = id_and_category[2].split(">")
                current_item["category"] = category[0].strip()
                current_item["check_item"] = category[1].strip() if len(category) > 1 else "N/A"
            else:
                current_item["category"] = "N/A"
                current_item["check_item"] = "N/A"

        # 결과 파싱
        elif line.startswith("※"):
            current_item["result"] = line.split("결과 :")[1].strip()

        # 상태 설명 추가
        elif current_item and "result" in current_item:
            if "details" not in current_item:
                current_item["details"] = line
            else:
                current_item["details"] += f" {line}"

    # 마지막 항목 저장
    if current_item:
        data.append(current_item)

    return data

def save_json_to_file(json_data, txt_file):
    # JSON 파일 이름 생성
    base_name = os.path.basename(txt_file)
    json_file = os.path.join("/tmp/results", f"{os.path.splitext(base_name)[0]}.json")
    
    # JSON 데이터 저장
    print(f"Saving JSON data to: {json_file}")  # 디버깅용 출력
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
    
    print(f"JSON 파일 저장 완료: {json_file}")
    return json_file

def upload_json(json_file, server_url):
    # JSON 파일 로드 후 업로드
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            json_data = json.load(file)

        print("Uploading JSON data:", json.dumps(json_data, ensure_ascii=False, indent=4))  # 디버깅용 출력
        response = requests.post(server_url, json=json_data, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print("JSON 데이터 업로드 성공!")
        else:
            print(f"업로드 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error during upload: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python3 parse_and_upload.py <txt_file> <server_url>")
        sys.exit(1)

    txt_file = sys.argv[1]
    server_url = sys.argv[2]

    print(f"Parsing TXT file: {txt_file}")  # 디버깅용 출력
    json_data = parse_txt_to_json(txt_file)
    json_file = save_json_to_file(json_data, txt_file)
    upload_json(json_file, server_url)
