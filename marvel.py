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
        G[node2][node1] = -1
    if node2 not in G[node1]:
        G[node1][node2] = -1
    G[node1][node2] = G[node1][node2] + 1
    G[node2][node1] = G[node2][node1] + 1
##    print '\t\t\t their strength is', G[node2][node1]
    
def countStrength(G, L):
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

marvelGraph, heroes = importMarvel('file')
##print len(heroes)

strengths = countStrength(marvelGraph, heroes)
##print strengths['4-D MAN/MERCURIO']

sortedStrengths = sorted(strengths.items(), key = lambda item: max(item[1].values()), reverse = True)
mostPopular1 = sortedStrengths[0]
mostPopular1Name = sortedStrengths[0][0]
print 'partner 1:', mostPopular1Name,

mostPopular1a = sorted(mostPopular1[1].items(), key = lambda item: item[1], reverse = True)
print 'appears with', mostPopular1a[0][0], 'in',mostPopular1a[0][1] ,'comics'



