import heapq
import pickle

def makeLink(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    G[node1][node2] = 1
    if node2 not in G:
        G[node2] = {}
    G[node2][node1] = 1

def importMarvel(file):
    G = {}
    L = []
    f = open(file, 'r')
    for line in f:
        q1 = line.find('"', 1)
        q2 = line.find('"', q1 + 1)
        hero, comic = line[1:q1], line[q2 + 1:-2]
        makeLink(G, hero, comic)
        if hero not in L:
            L.append(hero)
    return G, L

def makeWeightedLink(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        G[node2][node1] = 0
    if node2 not in G[node1]:
        G[node1][node2] = 0
    G[node1][node2] = G[node1][node2] + 1
    G[node2][node1] = G[node2][node1] + 1

def makeWeightedLink2(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        G[node2][node1] = 0
    if node2 not in G[node1]:
        G[node1][node2] = 0
    G[node1][node2] = G[node1][node2] + w
    G[node2][node1] = G[node2][node1] + w
    
def countLinks(G, L):
    strengths = {}
    for hero in L:
        for comic in G[hero]:
            for heroFriend in G[comic]:
                if hero != heroFriend:
                    makeWeightedLink(strengths, hero, heroFriend)
    return strengths

def makeWeights(ingraph):
    graph1 = {}
    graph2 = {}
    for hero in ingraph:
        for heroBuddy in ingraph[hero]:
            makeWeightedLink2(graph1, hero, heroBuddy, 1.0/ingraph[hero][heroBuddy])
            makeLink(graph2, hero, heroBuddy)
    return graph1, graph2

def dijkstra(G, v):
    inProgress = []
    heapq.heappush(inProgress, (0, v))

    inProgressDist = {}
    inProgressDist[v] = 0

    inProgressPath = {}
    inProgressPath[v] = [v]
    
    donePath = {}
    doneDist = {}

    while inProgress:
        distance, node = heapq.heappop(inProgress)
        donePath[node] = inProgressPath[node]
        del inProgressPath[node]
        doneDist[node] = distance

        for neighbor in G[node]:
            if neighbor not in doneDist:
                nextDistance = distance + G[node][neighbor]
                if neighbor not in inProgressDist:
                    heapq.heappush(inProgress, (nextDistance, neighbor))
                    inProgressPath[neighbor] = donePath[node] + [neighbor]
                    inProgressDist[neighbor] = nextDistance
                    
                elif nextDistance < inProgressDist[neighbor]:
                        inProgress.remove((inProgressDist[neighbor], neighbor))
                        inProgressDist[neighbor] = nextDistance
                        heapq.heappush(inProgress, (nextDistance, neighbor))
                        inProgressPath[neighbor] = donePath[node] + [neighbor]
    return doneDist, donePath
                

supers = ['SPIDER-MAN/PETER PAR',
'GREEN GOBLIN/NORMAN ',
'WOLVERINE/LOGAN ',
'PROFESSOR X/CHARLES ',
'CAPTAIN AMERICA']

superBuddies = ['HOARFROST/',
                'RAMPAGE/STUART CLARK',
                'STUART, BRIG. ALYSAN',
                'STUART, DR. ALISTAIR',
                'WHYTEOUT/STUART ANTH',
                'YAP']


inputPickle = open('margraph.pkl', 'rb')
graphs = pickle.load(inputPickle)
marvelWeighted = graphs[0]
marvelUn = graphs[1]
inputPickle.close()

print 'unpickled'

count = 0

for character in supers:
    superC = 0
    print character
    wD, wP = dijkstra(marvelWeighted, character)
    uD, uP = dijkstra(marvelUn, character)
    print 'distances and paths computed'
    for buddy in wD:
        if len(wP[buddy]) != len(uP[buddy]):
            superC += 1
    print superC
    count += superC 

print count

