import gp_alg.find_max_p
import gp_alg.comput_length
import gp_alg.compute_passengers
import gp_alg.find_min_deadline
import gp_alg.satisfy_capacity
def gp(graph,s_00,s_dd,beta,passengers,
       capacity,deadlines,speed, t1_max,t2_max,gamma,phi,M1):
    flag = True
    path = []
    while flag == True:

        max_stop = gp_alg.find_max_p.find_max_p(graph,s_00,s_dd,passengers,M1)
        if max_stop == 0:
            flag = False
            break

        path.append(max_stop)

        path_capacity = gp_alg.compute_passengers.compute_passengers(path, passengers)
        path_temp = [s_00] + path + [s_dd]
        path_length = gp_alg.comput_length.comput_length(path_temp,graph)
        path_min_deadline = gp_alg.find_min_deadline.find_min_deadline(path, deadlines)

        path_length_constraint = (path_min_deadline -path_capacity*(t2_max+t1_max))* speed

        if path_length > path_length_constraint or path_capacity > capacity:
            flag = False

            path.pop()
            break
        else:
            graph[max_stop, 0] = M1

    if len(path) > 0:
        gp_beta = 0
        for ii in path:
            gp_beta = gp_beta + beta[ii]
        gp_path = [s_00] + path + [s_dd]

        gp_path_length = gp_alg.comput_length.comput_length(gp_path,graph)
        gp_path_welfare = gp_beta - gp_path_length * gamma * phi
    else:
        gp_path_welfare, gp_path = 0, []
    return gp_path_welfare,gp_path