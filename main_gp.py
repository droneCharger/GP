
import gp_alg.construct_graph
import gp_alg.belong
import gp_alg.gp
def main_gp(k_b, number_data, capacity, s_00, s_dd, df, speed,passengers, beta, deadlines):

    M1 = 100000
    q = 1
    gamma = 0.15
    phi = 0.64
    graph_lat = df['lat'][0:number_data]
    graph_long = df['long'][0:number_data]

    graph0 = gp_alg.construct_graph.construct_graph(graph_lat, graph_long, number_data)

    t1_max, t2_max = 0.015, 0.015

    winner_set = []
    social_welfare_set = []
    graph = graph0
    while q <= k_b:

        social_welfare_final_path,final_path = \
                gp_alg.gp.gp(graph,s_00,s_dd,beta,passengers,
                        capacity,deadlines,speed, t1_max,t2_max,gamma,phi,M1)

        i2 = 1
        if len(final_path) > 0:
            while i2 < len(final_path):
                graph[final_path[i2],0] = M1
                i2 = i2 +1
            winner_set.append(final_path)
            social_welfare_set.append(social_welfare_final_path)
        q = q + 1

    rho = [0] * number_data
    sw_diff = [0] * number_data

    for stop in range(number_data):
        graph1 = gp_alg.construct_graph.construct_graph(graph_lat, graph_long, number_data)
        flag = gp_alg.belong.belong(stop, winner_set)
        rho_temp = 0
        if stop != s_00 and stop != s_dd and flag==1:
            graph1[stop,0] = M1
            for ilist in winner_set:
                if len(ilist) > 0:
                    winner_pay_set = []
                    social_welfare_pay_set = []
                    q_ = 1
                    while q_ <= k_b:

                        social_welfare_final_path_, final_path_ = \
                            gp_alg.gp.gp(graph1, s_00, s_dd, beta, passengers,
                                  capacity, deadlines, speed, t1_max, t2_max, gamma, phi, M1)
                              i2 = 1
                        while i2 < len(final_path_):
                            graph1[final_path_[i2], 0] = M1
                            i2 = i2 + 1
                        winner_pay_set.append(final_path_)
                        social_welfare_pay_set.append(social_welfare_final_path_)
                        q_ = q_ + 1  # 第二层while循环计数器

                    sw_winner = 0
                    sw_payment = 0
                    for i_1 in social_welfare_set:
                        sw_winner = sw_winner + i_1
                    for i_2 in social_welfare_pay_set:
                        sw_payment =sw_payment + i_2
                    sw_diff = sw_payment - sw_winner
                    rho_temp = rho_temp + max(0, sw_diff + beta[stop])

        rho[stop] = rho_temp
   total_social_welfare = 0
    for i3 in social_welfare_set:
        total_social_welfare = total_social_welfare + i3
   total_rho = 0
    for i4 in rho:
        total_rho = total_rho + i4
    number_winner = 0
    for i5 in winner_set:
        number_winner = number_winner + len(i5) - 2
    return total_social_welfare,total_rho,number_winner