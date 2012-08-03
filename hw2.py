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
##    print '\t\t', node1, 'is friends with', node2
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
##    print '\t\t\t their strength is', G[node2][node1]

def makeWeightedLink2(G, node1, node2, w):
##    print '\t\t', node1, 'is friends with', node2
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
##    print '\t\t\t their strength is', G[node2][node1]
    
def countLinks(G, L):
    strengths = {}
    for hero in L:
##        print hero
        for comic in G[hero]:
##            print '\t', comic
            for heroFriend in G[comic]:
##                print '\t plus', heroFriend
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

def dijkstra(G,v):
    dist_so_far = []
    dist_so_dict = {}
    heapq.heappush(dist_so_far, (0, v))
    dist_so_dict[v] = 0
    
    final_dist = {}
    
    paths_so_far = {}
    paths = {}
    paths_so_far[v] = [v]
    
    while dist_so_far: #len(final_dist) < len(G):
        nodeWithDist = heapq.heappop(dist_so_far)
        w = nodeWithDist[1]
        del dist_so_dict[w]
        final_dist[w] = nodeWithDist[0]
        paths[w] = paths_so_far[w]
##        print 'finalizing', w, '. dist = ', final_dist[w]
        
        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_dict:
                    dist_so_dict[x] = final_dist[w] + G[w][x]
                    heapq.heappush(dist_so_far, (final_dist[w] + G[w][x], x))
                    paths_so_far[x] = paths[w] + [x]
##                    print '\t found', x,'. dist =', dist_so_dict[x]
                elif final_dist[w] + G[w][x] < dist_so_dict[x]:
                    dist_so_far.remove((dist_so_dict[x], x))
                    dist_so_dict[x] = final_dist[w] + G[w][x]
                    heapq.heappush(dist_so_far, (final_dist[w] + G[w][x], x))
                    paths_so_far[x] = paths[w] + [x]
##                    print '\t relaxing', x, '. dist =', dist_so_dict[x]
    print 'lengths:', len(final_dist), ',', len(G)
    return paths, final_dist

supers = ['SPIDER-MAN/PETER PAR',
'GREEN GOBLIN/NORMAN ',
'WOLVERINE/LOGAN ',
'PROFESSOR X/CHARLES ',
'CAPTAIN AMERICA']

graphWithComics, heroList = importMarvel('file')
print 'file loaded'
graphWithCounts = countLinks(graphWithComics, heroList)
print 'comics counted'
marvelWeighted, marvelUn = makeWeights(graphWithCounts)
print 'weights computed'

count = 0
mismatchedHeroes = {}

for super in supers:
    shortestW, distancesW = dijkstra(marvelWeighted, super)
    shortestU, distancesU = dijkstra(marvelUn, super)
    mismatchedHeroes[super] = []
    superBuddies = ['HOARFROST/',
                    'RAMPAGE/STUART CLARK',
                    'STUART, BRIG. ALYSAN',
                    'STUART, DR. ALISTAIR',
                    'WHYTEOUT/STUART ANTH',
                    'YAP']
##    print 'from', super
##    print len(shortestU), len(shortestW), len(distancesU), len(distancesW)
    heroCount = 0
    heroNotCount = 0
    for superBuddy in shortestU:
##        print '\t to', superBuddy, 'takes', distancesU[superBuddy], '(unweighted) and ', distancesW[superBuddy], '(weighted)'
##        print '\t\t via (unweighted): ', shortestU[superBuddy]
##        print '\t\t via (weighted): ', shortestW[superBuddy]
        if len(shortestU[superBuddy]) != len(shortestW[superBuddy]):
            heroCount += 1
##            print 'Tone. I\'ve got tone.'
            mismatchedHeroes[super].append(superBuddy)
        else:
            heroNotCount += 1
##            print 'No joy. Paths match.'
    print super, ':', heroCount, 'of', heroCount + heroNotCount
    count += heroCount

##output = open('hero.pkl', 'wb')
##pickle.dump(mismatchedHeroes, output)
##output.close()
print count



