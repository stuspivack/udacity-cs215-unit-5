import heapq
from pprint import pprint

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def importMovieFileOld(filename):
    G = {}
    actors = []
    movies = []
    f = open(filename, 'r')
    actornumber = 0
    movienumber = 1
    for line in f:
        actor, foo, movie = line.partition('\t')
        actor = actor.strip()
        movie = movie.strip()
        if movie not in movies:
            movies.append(movie)
            thismovie = movienumber
            movienumber += 2
        else:
            thismovie = 2 * movies.index(movie) + 1
        if actor not in actors:
            thisactor = actornumber
            actors.append(actor)
            actornumber += 2
        else:
            thisactor = 2 * actors.index(actor)
        if actornumber % 1000 == 0: print actornumber
        make_link(G, thisactor, thismovie)
    return G, actors, movies

def importMovieFile(filename):
    G = {}
    f = open(filename, 'r')
    actors = []
    movies = []
    for line in f:
        actor, foo, movie = line.partition('\t')
        actor = actor.strip()
        movie = movie.strip()
        actors.append(actor)
        movies.append(movie)
        make_link(G, actor, movie)
    return G, actors, movies

def importObscurity(filename):
    D = {}
    f = open(filename, 'r')
    for line in f:
        movie, foo, weight = line.rpartition('\t')
        movie = movie.strip()
        D[movie] = float(weight)
    return D

def maxObs(G, obsDict, path):
    return max([obsDict.get(movie, 0) for movie in path])

def dijkstra(G, obscurityDict,v):
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
##                    dist_so_dict[x] = final_dist[w] + G[w][x]
##                    heapq.heappush(dist_so_far, (final_dist[w] + G[w][x], x))
##                    paths_so_far[x] = paths[w] + [x]
                    dist_so_dict[x] = maxObs(G, obscurityDict, paths[w] + [x])
                    heapq.heappush(dist_so_far, (maxObs(G, obscurityDict, paths[w] + [x]), x))
                    paths_so_far[x] = paths[w] + [x]
##                    print '\t found', x,'. dist =', dist_so_dict[x]
                elif maxObs(G, obscurityDict, paths[w] + [x]) < dist_so_dict[x]:
                    dist_so_far.remove((dist_so_dict[x], x))
                    dist_so_dict[x] = maxObs(G, obscurityDict, paths[w] + [x])
                    heapq.heappush(dist_so_far, (maxObs(G, obscurityDict, paths[w] + [x]), x))                    
                    paths_so_far[x] = paths[w] + [x]
##                    print '\t relaxing', x, '. dist =', dist_so_dict[x]
    return paths, final_dist

test = {(u'Ali, Tony', u'Allen, Woody'): 0.5657,
        (u'Auberjonois, Rene', u'MacInnes, Angus'): 0.0814,
        (u'Avery, Shondrella', u'Dorsey, Kimberly (I)'): 0.7837,
        (u'Bollo, Lou', u'Jeremy, Ron'): 0.4763,
        (u'Byrne, P.J.', u'Clarke, Larry'): 0.109,
        (u'Couturier, Sandra-Jessica', u'Jean-Louis, Jimmy'): 0.3649,
        (u'Crawford, Eve (I)', u'Cutler, Tom'): 0.2052,
        (u'Flemyng, Jason', u'Newman, Laraine'): 0.139,
        (u'French, Dawn', u'Smallwood, Tucker'): 0.2979,
        (u'Gunton, Bob', u'Nagra, Joti'): 0.2136,
        (u'Hoffman, Jake (I)', u'Shook, Carol'): 0.6073,
        (u'Kamiki, Ry\xfbnosuke', u'Thor, Cameron'): 0.3644,
        (u'Roache, Linus', u'Dreyfuss, Richard'): 0.6731,
        (u'Sanchez, Phillip (I)', u'Wiest, Dianne'): 0.5083,
        (u'Sheppard, William Morgan', u'Crook, Mackenzie'): 0.0849,
        (u'Stan, Sebastian', u'Malahide, Patrick'): 0.2857,
        (u'Tessiero, Michael A.', u'Molen, Gerald R.'): 0.2056,
        (u'Thomas, Ken (I)', u'Bell, Jamie (I)'): 0.3941,
        (u'Thompson, Sophie (I)', u'Foley, Dave (I)'): 0.1095,
        (u'Tzur, Mira', u'Heston, Charlton'): 0.3642}

answer = {(u'Boone Junior, Mark', u'Del Toro, Benicio'): None,
          (u'Braine, Richard', u'Coogan, Will'): None,
          (u'Byrne, Michael (I)', u'Quinn, Al (I)'): None,
          (u'Cartwright, Veronica', u'Edelstein, Lisa'): None,
          (u'Curry, Jon (II)', u'Wise, Ray (I)'): None,
          (u'Di Benedetto, John', u'Hallgrey, Johnathan'): None,
          (u'Hochendoner, Jeff', u'Cross, Kendall'): None,
          (u'Izquierdo, Ty', u'Kimball, Donna'): None,
          (u'Jace, Michael', u'Snell, Don'): None,
          (u'James, Charity', u'Tuerpe, Paul'): None,
          (u'Kay, Dominic Scott', u'Cathey, Reg E.'): None,
          (u'McCabe, Richard', u'Washington, Denzel'): None,
          (u'Reid, Kevin (I)', u'Affleck, Rab'): None,
          (u'Reid, R.D.', u'Boston, David (IV)'): None,
          (u'Restivo, Steve', u'Preston, Carrie (I)'): None,
          (u'Rodriguez, Ramon (II)', u'Mulrooney, Kelsey'): None,
          (u'Rooker, Michael (I)', u'Grady, Kevin (I)'): None,
          (u'Ruscoe, Alan', u'Thornton, Cooper'): None,
          (u'Sloan, Tina', u'Dever, James D.'): None,
          (u'Wasserman, Jerry', u'Sizemore, Tom'): None}

MovieGraph, actorList, movieList = importMovieFile('imdb-1.tsc')
obscurityDict = importObscurity('imdb-weights.tsv')

##paths, distances = dijkstra(MovieGraph, obscurityDict, u'Ali, Tony')
##print distances[u'Allen, Woody']

testOut = {}
for t in test:
    paths, distances = dijkstra(MovieGraph, obscurityDict, t[0])
    testOut[t] = distances[t[1]]
    pprint(testOut)
    
pprint(testOut)
    
