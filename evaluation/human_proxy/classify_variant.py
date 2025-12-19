# Task: classify a tagged value (modeled as (tag, payload))

def classify(v: tuple[str, object]) -> str:
    tag, payload = v
    if tag == "Ok":
        return "ok:" + str(payload)
    if tag == "Err":
        return "err:" + str(payload)
    return "unknown"

print(classify(("Ok", 41)))
