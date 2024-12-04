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
            if current_item:  # 현재 항목 저장
                data.append(current_item)
            current_item = {}

            # ID 및 중요도 추출
            id_and_category = line.split("|")
            current_item["id"] = id_and_category[0].split("▶")[-1].strip()
            current_item["importance"] = id_and_category[1].strip("()").strip()
            category = id_and_category[2].split(">")

            # 카테고리와 점검 항목
            current_item["category"] = category[0].strip()
            current_item["check_item"] = category[1].strip()

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
