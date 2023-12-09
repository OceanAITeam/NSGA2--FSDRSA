import numpy as np
import pymysql
from algorithms import algorithm_1
from decoder import get_scheme_perform

if __name__ == '__main__':
    dbhost='localhost'
    dbuser='root'
    dbpass='123456'
    dbname='xu'
    db=pymysql.connect(host=dbhost,user=dbuser,password=dbpass,database=dbname)

    cursor = db.cursor()
    cursor.execute("select * from refrigerator")
    data = list(cursor.fetchall())
    db.close()

    info = []
    relate = []
    for ele in data:
        info.append(list(ele[2:5]))
        temp = []
        for ele_ in ele[-1].split('，'):
            if ele_=='/':
                temp.append(0)
            else:
                temp.append(int(ele_))
        relate.append(temp)
    info = np.array(info,dtype=int)
    time = info[:,0]
    need = info[:,1]
    danger = info[:,2]
    num_of_part = len(time)

    constr_mat = np.zeros(shape = (num_of_part,num_of_part))

    for i, successor in enumerate(relate):
        for ele in successor:
            if ele!=0:
                constr_mat[i, np.array(ele)-1] = 1

    disassembly_side = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

    dis_seq = algorithm_1(constr_mat, num_of_part, constr_mat, disassembly_side, danger, need,
                   popnum = 100, crossover_prob = 0.85, mutation_prob = 0.25,
                   evolution_time = 10)
    schemes, performance = get_scheme_perform(dis_seq, data, danger, need, num_of_part)

    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()

    cursor.execute("select * from s")
    data = list(cursor.fetchall())
    if data:
        cursor.execute("truncate table s")

    sql = "insert into s (disschemem, dangerindex, demandindex) values (%s,%s,%s)"
    # param=(23456,'lilei',20)
    for i in range(len(schemes)):
        cursor.execute(sql, (str(schemes[i]), str(performance[i][0]), str(performance[i][1])))
    db.commit()
    db.close()