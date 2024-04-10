n, q = map(int, input().split()) # n = 채팅방 수, q 명령 수
inputlist = list(map(int, input().split()))
parent = [0] + inputlist[1:n+1] # 부모 채팅방 번호
authority = [0] + inputlist[n+1:] # 권한 세기
alarm = [True]*(n+1) # 알람 온오프
children = [[] for _ in range(n+1)]

def init() :
    for node in range(0, n+1):
        children[parent[node]].append(node)
    return children

def find_available_chat(c, children, root) :
    # c에 대해서 알림에 도달할 수 있는 하위 채팅방 개수 구하기
    answer = 0
    nodes = []
    cnt = 1
    for i in children[c] :
        if alarm[i] == True and authority[i] >= cnt :
            nodes.append(i)
            answer += 1
    # nodes = 가능한 채팅방을 넣는 리스트 [3, 4]

    while nodes :
        cnt += 1
        new_nodes = []
        for i in nodes :
            for j in children[i] :
                if alarm[j] == False :
                    continue 
                if authority[j] >= cnt :
                    answer += 1
                    new_nodes.append(j)
                else :
                    new_nodes.append(j)
        nodes = new_nodes

    return answer

children = init()
for _ in range(q-1) :
    order = list(map(int, input().split()))
    if order[0] == 200 :
        c = order[1]
        if alarm[c] :
            alarm[c] = False
        else :
            alarm[c] = True
    elif order[0] == 300 :
        c, power = order[1], order[2]
        authority[c] = power
    elif order[0] == 400 :
        c1, c2 = order[1], order[2]
        a, b = parent[c1], parent[c2]
        children[a].remove(c1)
        children[b].remove(c2)
        children[a].append(c2)
        children[b].append(c1)
        parent[c1], parent[c2] = b, a
    elif order[0] == 500 :
        c = order[1]
        cnt = find_available_chat(c, children, 1)
        print(cnt)