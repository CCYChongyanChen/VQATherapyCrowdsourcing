import json
q_ids = []
folderpath = "../annotations/"

groups_origin=folderpath+"train_mostcommon_sub_rand.json"

groups_with_ad=folderpath+"train_mostcommon_sub_rand_w_ad.json"
groups_wo_ad=folderpath+"train_mostcommon_sub_rand_wo_ad.json"


wpath = folderpath+"diff_qids.json"

def get_qid_Answer_Diff():
    splits = ["val","test","train"]#"train",
    with open(wpath,'w',encoding="utf-8") as json_file_all:
        for split in splits:
            # unanswerable_MostCommon(answerpath,AtLeastTwoAgreementspath)
            # Qid2Q1(questionpath,Qid2Qpath)
            # Qid2Q2(AtLeastTwoAgreementspath,Qid2Qpath,Qid2Qpath2)
            # filter_Questions(Qid2Qpath2, Wpath, random_path,random_i_path, randomFlag=True)
            # find_unique_answer(random_path)
            answer_difference_path = folderpath + "VQA_ans_diff_"+split+".json"
            with open(answer_difference_path,encoding="utf-8") as json_file_diff:
                    datas = json.load(json_file_diff)
                    for data in datas:
                        q_ids.append(data["qid"])
        json.dump(q_ids,json_file_all)
        print(len(q_ids))
def get_w_wo_diff_files():
    w_diff_list=[]
    wo_diff_list=[]        
    # open vqa-answer-diff qids
    with open(wpath ,encoding="utf-8") as json_file_diff:
        qids = json.load(json_file_diff)
    print(qids)

    with open(groups_origin,encoding="utf-8") as json_file_origin:
        datas = json.load(json_file_origin)
        for data in datas:
            if str(data["qid"]) in qids:
                w_diff_list.append(data)
            else:
                wo_diff_list.append(data)            


    with open(groups_with_ad,'w',encoding="utf-8") as json_w_ad:
        json.dump(w_diff_list,json_w_ad)
    with open(groups_wo_ad,'w',encoding="utf-8") as json_wo_ad:
        json.dump(wo_diff_list,json_wo_ad)

    print(len(wo_diff_list),len(w_diff_list))
    ##154516, 9215;
    

def Random_Index(random_path,group_answers):
    with open(random_path,encoding="utf-8") as json_file_gr:
        with open(group_answers,'w',encoding="utf-8") as json_file_gw:
            datas = json.load(json_file_gr)
            group=[datas[i:i+5] for i in range(0, len(datas), 3)]
            json.dump(group,json_file_gw)

w_groups_with_ad=folderpath+"train_grouped.json"
w_groups_wo_ad=folderpath+"train_grouped_wo_diff.json"

Random_Index(groups_with_ad,w_groups_with_ad)
Random_Index(groups_wo_ad,w_groups_wo_ad)