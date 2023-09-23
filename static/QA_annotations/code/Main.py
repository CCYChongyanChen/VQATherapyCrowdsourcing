import json
import os
import sys
import re
from Preprocess import processed_answer
from subquestions import filter_Questions

def MoreThanOnce(List): 
    counter = 4
    num = None
    newList=[]
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> 1): 
            newList.append(i)
        
        # if (curr_frequency>4):
        #     return None
    FinalList = list(set(newList))
    # if len(FinalList) ==1: # discuss this
        # if (List.count(FinalList[0]))>4:
        #     return None
    return FinalList
        

def find_unique_answer(path):
    allCount2=0
    allCount3=0
    allCount4=0
    allCount5=0
    with open(path,encoding="utf-8") as json_file:
        datas = json.load(json_file)
        for data in datas:
            lenanswers=(len(data["answers"]))
            if lenanswers == 2:
                allCount2+=1
            if lenanswers ==3:
                allCount3+=1
            if lenanswers ==4:
                allCount4+=1
            if lenanswers ==5:
                allCount5+=1
    print(allCount2,allCount3,allCount4,allCount5)


def Qid2Q1(questionpath,Qid2Qpath):
    with open(questionpath,encoding="utf-8") as question_json_file:
        with open(Qid2Qpath,'w',encoding="utf-8") as json_file_w1:
            tmp_ann={}
            question_datas = json.load(question_json_file)    
            for question_data in question_datas["questions"]:
                tmp_ann[question_data["question_id"]]=question_data["question"]
            json.dump(tmp_ann,json_file_w1)


def Qid2Q2(AtLeastTwoAgreementspath,Qid2Qpath1,Qid2Qpath2):
    
    final_data = []
    with open(AtLeastTwoAgreementspath,encoding="utf-8") as answers_json_file:
        with open(Qid2Qpath1,encoding="utf-8") as question_json_file:
            with open(Qid2Qpath2,'w',encoding="utf-8") as json_file_w:
                datas = json.load(answers_json_file)                    
                question_datas = json.load(question_json_file)    
                for data in datas:
                    tmp_ann={}  

                    qid = data["question_id"]
                    tmp_ann["question_id"]=qid
                    # try:
                    tmp_ann["question"]=question_datas[str(qid)]
                    # except:
                    # print(qid)
                    tmp_ann["answers"]=data["answers"]
                    tmp_ann["image"]=data["image"]
                    tmp_ann["answer_type"]=data["answer_type"]
                    final_data.append(tmp_ann)
                json.dump(final_data,json_file_w)

def unanswerable_MostCommon(answerpath,mostcommonpath):
    
    count=0
    count_vq_answerable=0
    count_noOverlap_Or_noDifference=0
    MostCommon_ann=[]
    count_mostcommon=0
    with open(answerpath,encoding="utf-8") as answer_json_file:
        with open(mostcommonpath,'w',encoding="utf-8") as json_file_w:
            answers_datas = json.load(answer_json_file)
            for answer_data in answers_datas["annotations"]:
                # answer_data["question_id"]
                
                tmp_ann={}
                # unanswerable questions
                tmp_answers=[i['answer'] for i in answer_data["answers"]]
                answerable_answers=list(filter(lambda x:x!="unsuitable" and x!="unsuitable image" and x!="unanswerable",tmp_answers))
                p_answerable_answers=processed_answer(answerable_answers)
                # filtering answers; if at least two workers agree on it, then keep it.
                AnswersMoreThanOnce=MoreThanOnce(p_answerable_answers)
                # if (AnswersMoreThanOnce is None) :
                #     count_mostcommon+=1
                # else: 
                if (len(AnswersMoreThanOnce)<2):
                    count_noOverlap_Or_noDifference+=1
                else:
                    
                    count+=1
                    tmp_ann["answers"]=AnswersMoreThanOnce
                    tmp_ann["image"]=answer_data["image_id"]
                    tmp_ann["question_id"]=answer_data["question_id"]
                    tmp_ann["answer_type"]=answer_data["answer_type"]
                    MostCommon_ann.append(tmp_ann)
            
            json.dump(MostCommon_ann,json_file_w)
    print("count: ",count)
    print("countnoverlap:",count_noOverlap_Or_noDifference)





def Random_Index(random_path,group_answers):
    with open(random_path,encoding="utf-8") as json_file_gr:
        with open(group_answers,'w',encoding="utf-8") as json_file_gw:
            datas = json.load(json_file_gr)
            group=[datas[i:i+5] for i in range(0, len(datas), 3)]
            json.dump(group,json_file_gw)

if __name__ == "__main__":
    """===========================================================
            Use for generating
    ============================================================="""
    
    splits = ["train"]#"train",
    folderpath = "../annotations/"
    for split in splits:
        folderpath = "../annotations/"
        answerpath=folderpath+"v2_mscoco_"+split+"2014_annotations.json"
        questionpath = folderpath+"v2_OpenEnded_mscoco_"+split+"2014_questions.json"
        AtLeastTwoAgreementspath=folderpath+split+"_two_agreements.json"
        Qid2Qpath=folderpath+split+"_qid_2_q.json"
        Qid2Qpath2=folderpath+split+"_two_agreements_qid_2_q.json"
        Wpath=folderpath+split+"_mostcommon_sub.json"
        random_path=folderpath+split+"_mostcommon_sub_rand.json"
        random_i_path=folderpath+split+"_mostcommon_sub_rand_index.json"
        group_answers=folderpath+split+"_grouped.json"
        # # process
        
        unanswerable_MostCommon(answerpath,AtLeastTwoAgreementspath)
        Qid2Q1(questionpath,Qid2Qpath)
        Qid2Q2(AtLeastTwoAgreementspath,Qid2Qpath,Qid2Qpath2)
        filter_Questions(Qid2Qpath2, Wpath, random_path,random_i_path, randomFlag=True)
        find_unique_answer(random_path)



    
    groups_with_ad=folderpath+"train_mostcommon_sub_rand_w_ad.json"
    groups_wo_ad=folderpath+"train_mostcommon_sub_rand_wo_ad.json"
    Random_Index(random_path,group_answers)
