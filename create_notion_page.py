import json, sys, urllib.request, urllib.error, os

def create_page(json_file):
    token = os.environ["NOTION_TOKEN"]
    parent_id = "355e447c4b6480889b85e4de05f0d4b2"

    with open(json_file, encoding="utf-8") as f:
        d = json.load(f)

    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"text": {"content": d.get("title", "")}}]}
        },
        "children": [
            {"object": "block", "type": "callout", "callout": {
                "rich_text": [{"text": {"content": d.get("summary", "")}}],
                "icon": {"emoji": "\U0001f4a1"}
            }},
            {"object": "block", "type": "divider", "divider": {}},
            {"object": "block", "type": "heading_3", "heading_3": {
                "rich_text": [{"text": {"content": "\U0001f4cc 놓치면 아까운 것 TOP 3"}}]
            }},
            {"object": "block", "type": "numbered_list_item", "numbered_list_item": {
                "rich_text": [{"text": {"content": d.get("top1", "")}}]
            }},
            {"object": "block", "type": "numbered_list_item", "numbered_list_item": {
                "rich_text": [{"text": {"content": d.get("top2", "")}}]
            }},
            {"object": "block", "type": "numbered_list_item", "numbered_list_item": {
                "rich_text": [{"text": {"content": d.get("top3", "")}}]
            }}
        ]
    }

    req = urllib.request.Request(
        "https://api.notion.com/v1/pages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print("SUCCESS:", result.get("id"))
    except urllib.error.HTTPError as e:
        print("HTTP ERROR:", e.code, e.read().decode())
        sys.exit(1)
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)

if __name__ == "__main__":
    create_page(sys.argv[1])
