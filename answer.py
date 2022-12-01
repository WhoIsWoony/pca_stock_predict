import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from math import pow

# cp : 클러스터 별 종가 데이터, name: 클러스터 별 기업 이름, num: 클러스터 고유번호
def plot_cluster_cpdata(cp, name, num):
    plt.title("Closing Price Data - Cluster #" + str(num))
    plt.xlabel("Date/Month")
    plt.xticks(np.arange(0, 248, step=41),
               ["2020-01", "2020-03", "2020-05", "2020-07", "2020-09", "2020-11", "2021-01"])
    plt.ylabel("Closing Price/won")

    colors = ['Blue', 'Red', 'Green', 'Black', 'Orange',
              'LightBlue', 'LightGreen', 'Grey']
    targets = name
    colors = colors[:len(name)]

    plt.rc('font', family='Malgun Gothic')
    for i, p in enumerate(cp):
        plt.plot(p, color=colors[i])
    plt.legend(targets)
    plt.savefig("C:/Users/swslo/Desktop/학기/4학년 2학기/"
                "수치해석/4차 과제_주가 데이터/savefig/Closing Price Data - Cluster #" + str(num) + ".png")
    plt.show()


# f: feture vectors, cltd: cluster dictionary, n: the number of cluster, ctrd: centeroid, iter: clustering count
def plot_result_of_clustering(f, cltd, n, ctrd, iter):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('Result of clustering - iter: ' + str(iter), fontsize=20)

    targets = [0] * (n*2)
    targets[:n] = ["Centeroid" + str(i+1) for i in range(n)]
    targets[n:] = ['Cluster' + str(i+1) for i in range(n)]
    colors = ['Blue', 'Red', 'Green', 'Black', 'Orange', 'LightBlue',
              'LightBlue', 'Orange', 'LightGreen', 'Grey', 'Red', 'Blue']
    for i in range(n):
        ax.scatter(ctrd[i][0], ctrd[i][1], c=colors[i], s=200, marker='x')
    for i in range(n):
        company = cltd["cluster"+str(i+1)][0]
        ax.scatter(f[company][0], f[company][1], c=colors[i+n], s=20)
    for i in range(n):
        companies = cltd["cluster"+str(i+1)]
        for company in companies[1:]:
            ax.scatter(f[company][0]
                       , f[company][1]
                       , c=colors[i+n]
                       , s=20)
    ax.legend(targets)
    ax.grid()
    plt.savefig("C:/Users/swslo/Desktop/학기/4학년 2학기/"
                "수치해석/4차 과제_주가 데이터/savefig/Result_of_Clustering#" + str(iter) + "_N_" + str(n) + ".png")
    plt.show()

# Set CP data
cpData = np.zeros((248, 584), int) # 기업 584개의 개장일 수 248
i = 0
fr = open("./krx300_cp_list.txt", 'r')
fr2 = open("./company_name.txt", 'r', encoding="UTF-8")
company_name = []
while True:
    line = fr.readline()
    if not line: break
    cp = line.split(' ')
    if cp[0] is not '\n':
        cpData[:, i] = cp[:248]
        i += 1
        company_name.append(fr2.readline()[:-1])

fr.close()

fr = open("./etf_cp_list.txt", 'r')
while True:
    line = fr.readline()
    if not line: break
    cp = line.split(' ')
    if cp[0] is not '\n':
        cpData[:, i] = cp[:248]
        i += 1
        company_name.append(fr2.readline()[:-1])

fr.close()
fr2.close()

# Preprocessing
input_data = np.zeros((248, 584), float) # 일일 변화량으로 전처리
for i in range(584):
    yesterdayCP = cpData[0][i]
    for j, todayCP in enumerate(cpData[:, i]):
        input_data[j][i] = 100*(todayCP/yesterdayCP - 1)
        yesterdayCP = todayCP

# feature vector 2개로 차원 축소 했을 때 전체 feature 대비 두 vector의 기여도
"""
cov_matrix = np.cov(input_data)
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
v = []
s = np.sum(eigenvalues)
for _v in eigenvalues:
    v.append(_v/s)
print(str(np.sum(v[:2]) * 100 + 0.05)[:4])
"""

# feature vector: 2 // 전체 feature 중 약 24.6% 기여
pca = PCA(n_components=2)
fvs = pca.fit_transform(input_data.T) # feature vectors (548, 2)

# 초기 centeroid 세팅
f0min = min(fvs[:, 0])
f0max = max(fvs[:, 0])
f0half = (f0min + f0max) / 2
f1min = min(fvs[:, 1])
f1max = max(fvs[:, 1])
f1_a_third = f1min + (f0max - f1min) / 3
f1_two_thirds = f1max - (f0max - f1min) / 3

centeroid = np.zeros((6,2),float)
centeroid[0] = [(f0min+f0half)/2, (f1min+f1_a_third)/2]
centeroid[1] = [(f0min+f0half)/2, (f1_a_third+f1_two_thirds)/2]
centeroid[2] = [(f0min+f0half)/2, (f1_two_thirds+f1max)/2]
centeroid[3] = [(f0half+f0max)/2, (f1min+f1_a_third)/2]
centeroid[4] = [(f0half+f0max)/2, (f1_a_third+f1_two_thirds)/2]
centeroid[5] = [(f0half+f0max)/2, (f1_two_thirds+f1max)/2]


cluster_n = 6 #cluster 개수
iter = 10 # 클러스터링 알고리즘 반복 횟수
for it in range(iter):
    # 클러스터 별 분류된 기업의 인덱스 저장 dict
    cluster_dict = {"cluster" + str(i + 1): [] for i in range(cluster_n)}

    #update clusters
    for i in range(584):
        # L2 distance - 제곱근 수행 x
        min_distance_square = pow(centeroid[0][0]-fvs[i][0], 2) + pow(centeroid[0][1]-fvs[i][1], 2)
        cluster_name = "cluster1"
        for j in range(1, cluster_n):
            new_distance = pow(centeroid[j][0]-fvs[i][0], 2) + pow(centeroid[j][1]-fvs[i][1], 2)
            if min_distance_square > new_distance:
                min_distance_square = new_distance
                cluster_name = "cluster" + str(j+1)
        cluster_dict[cluster_name].append(i)
    # 반복 횟수 별 클러스터링 결과 출력
    #plot_result_of_clustering(fvs, cluster_dict, cluster_n, centeroid, it+1)

    # update centeroid vectors
    for i in range(cluster_n):
        f0_centeroid = 0
        f1_centeroid = 0
        cnt = 0
        for cnum in cluster_dict["cluster"+str(i+1)]: # cnum : unique number of company
            f0_centeroid += fvs[cnum][0]
            f1_centeroid += fvs[cnum][1]
            cnt += 1
        centeroid[i] = [f0_centeroid/cnt, f1_centeroid/cnt]

# 클러스터 별 분류된 기업들의 종가 데이터 저장
cluster_cpData = {"cluster" + str(i + 1):
                      np.zeros((len(cluster_dict["cluster"+str(i+1)])+1, 248), float) for i in range(cluster_n)}
CCPk = [0]*248
for i in range(cluster_n):
    companies = cluster_dict["cluster"+str(i+1)]
    for j, company in enumerate(companies):
        cluster_cpData["cluster"+str(i+1)][j] = cpData[:, company]
        temp = [x+y for x,y in zip(CCPk, cpData[:, company])]
        CCPk = temp
    temp = [x/j for x in CCPk]
    CCPk = temp
    cluster_cpData["cluster"+str(i+1)][-1] = CCPk # 각 클러스터 별 마지막 인덱스에 CCPk값 저장

# 클러스터 별 분류된 기업들의 베타 계수 저장
cluster_Beta = {"cluster" + str(i + 1):
                      np.zeros((len(cluster_dict["cluster"+str(i+1)])), float) for i in range(cluster_n)}
for i in range(cluster_n):
    clusterK_beta = cluster_Beta["cluster" + str(i+1)]
    clusterK = cluster_cpData["cluster"+str(i+1)]
    CCPk = clusterK[-1]
    var_CCPk = np.var(clusterK[-1])
    for i, CP in enumerate(clusterK[:-1]):
        cov_CCPk_CP = np.cov(CCPk, CP)[0][1]
        clusterK_beta[i] = cov_CCPk_CP / var_CCPk

# 클러스터 별 최대 7개의 기업들만 선정하여 종가, 종목 명, 베타 계수 출력
for i in range(cluster_n):
    cluster_name = "cluster"+str(i+1)
    k = len(cluster_Beta[cluster_name])
    if k > 8: k = 7

    clusterK_cp = np.zeros((k+1, 248))
    clusterK_cp[:k] = cluster_cpData[cluster_name][:k]
    clusterK_cp[-1] = cluster_cpData[cluster_name][-1] #CCPk
    clusterK_name = []
    for j in range(k):
        beta = cluster_Beta[cluster_name][j] + 0.0005
        if beta > 10: beta = str(beta)[:6]
        else: beta = str(beta)[:5]
        clusterK_name.append(str(company_name[cluster_dict[cluster_name][j]]) + '-' + beta)
    clusterK_name.append("CCPk - None")
    #plot_cluster_cpdata(clusterK_cp, clusterK_name, i+1)
