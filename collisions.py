def detect_collisions(x1, y1, w1, h1, x2, y2, w2, h2):
    ans = False
    if (x2 <= x1 <= x2 + w2 or x2 <= x1 + w1 <= x2 + w2) and (y2 <= y1 <= y2 + h2 or y2 <= y1 + h1 <= y2 + h2):
        ans = True
    elif x2 <= x1 + w1 // 2 <= x2 + w2 // 2 and y2 <= y1 + h1 // 2 <= y2 + h2:
        ans = True
    elif x2 <= x1 + w1 <= x2 + w2 // 2 and y2 <= y1 + h1 // 2 <= y2 + h2 // 2:
        ans = True
    elif x2 <= x1 + w1 // 2 <= x2 + w2 and y2 <= y1 + h1 // 2 <= y2 + h2:
        ans = True
    return ans
