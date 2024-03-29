from django.http import JsonResponse
from ResModel.models import HubUser, Researcher, Relationship, Collection
from ResModel.models import ProjectAuthor, Concern, ResInstitution, PaperAuthor


def getPersonalPortal(request):
    try:
        if request.method == "GET":
            userId = request.GET.get('userId')
            resId = request.GET.get('resId')
            if ((userId is not None) and (resId is not None)):

                researcher = Researcher.objects.get(ResId=resId)
                hubuser = HubUser.objects.get(UserEmail=userId)
                # resinstitution = ResInstitution.objects.get(ResId=resId)

                if((researcher is not None) and (hubuser is not None)):
                    # 浏览量加一
                    visitnumber = researcher.VisitNum + 1
                    researcher.VisitNum = visitnumber
                    Researcher.objects.filter(
                        ResId=resId).update(VisitNum=visitnumber)

                    res = {}

                    # is_have
                    try:
                        is_have = Researcher.objects.get(UserEmail=userId)
                        if(is_have is not None):
                            res['ishave'] = True
                        else:
                            res['ishave'] = False
                    except Exception as e:
                        res['ishave'] = False

                    # avatar
                    res['avatar'] = researcher.UserEmail.UserImage

                    # isClaimed
                    res['isclaimed'] = researcher.IsClaim

                    # isFollowing
                    try:
                        concern = Concern.objects.get(
                            UserEmail=userId, ResearchId=researcher.ResId)
                        if(concern is not None):
                            res['isfollowing'] = True
                        else:
                            res['isfollowing'] = False
                    except Exception as e:
                        res['isfollowing'] = False

                    # isMyPortal
                    try:
                        if(researcher.UserEmail_id == hubuser.UserEmail):
                            res['ismyportal'] = True
                        else:
                            res['ismyportal'] = False
                    except Exception as e:
                        res['ismyportal'] = False

                    # visitNum
                    res['visitnum'] = researcher.VisitNum

                    # followNum
                    try:
                        follow = Concern.objects.filter(
                            ResearchId=researcher.UserEmail_id).all()
                        if(follow is None):
                            res['follownum'] = 0
                        else:
                            res['follownum'] = follow.__len__()
                    except Exception as e:
                        res['follownum'] = 0

                    # realName
                    res['Resname'] = researcher.ResName

                    # insName
                    res['insname'] = resinstitution.InstitutionId.InsName

                    # insId
                    res['insid'] = resinstitution.InstitutionId_id

                    # mail
                    res['mail'] = researcher.UserEmail_id

                    # paperNum
                    res['papernum'] = researcher.LiteratureNum

                    # resField
                    res['resfield'] = researcher.ResField

                    # resCount & quoteNum & quoCount
                    try:
                        papersid = PaperAuthor.objects.filter(
                            ResearcherId=resId).all()
                        datas = [0, 0, 0, 0, 0, 0, 0, 0]
                        quotes = [0, 0, 0, 0, 0, 0, 0, 0]
                        quoteNum = 0
                        for i in papersid:
                            year = i.PaperId.PaperTime
                            index = 8 - (2020-year)
                            if(index < 0):
                                continue
                            datas[index] = datas[index] + 1
                            quotes[index] = quotes[index] + \
                                i.PaperId.PaperCitation
                            quoteNum = quoteNum + i.PaperId.PaperCitation
                        resCount = []
                        quoCount = []
                        for i in datas:
                            resCount.append(str(i))
                        for i in quotes:
                            quoCount.append(str(i))
                        res['rescount'] = resCount
                        res['quocount'] = quoCount
                        res['quotenum'] = str(quoteNum)
                    except Exception as e:
                        res['rescount'] = [
                            '0', '0', '0', '0', '0', '0', '0', '0']
                        res['quocount'] = [
                            '0', '0', '0', '0', '0', '0', '0', '0']
                        res['quotenum'] = '0'
                    # magCount ....
                    try:
                        projectauthor = ProjectAuthor.objects.filter(
                            ResearcherId=resId).all()
                        confCount = projectauthor.__len__()
                        magCount = papersid.__len__()
                        all_have = projectauthor.__len__() + papersid.__len__()
                        magpar = str(
                            int(float(magCount)/float(all_have)*100))+'%'
                        confpar = str(
                            int(float(confCount)/float(all_have)*100))+'%'
                        res['magcount'] = magCount
                        res['magpar'] = magpar
                        res['confcount'] = confCount
                        res['confpar'] = confpar
                    except Exception as e:
                        res['magcount'] = 0
                        res['magpar'] = '0%'
                        res['confcount'] = 0
                        res['confpar'] = '0%'
                    # coopData
                    try:
                        count = 0
                        coopData = []
                        relationship = Relationship.objects.filter(
                            ResearchId1=resId).all()
                        for i in relationship:
                            if(coopData.__len__() == 5):
                                break
                            res_temp = {}
                            reseacher_relation = i.ResearchId2
                            resinstitution_temp = ResInstitution.objects.get(
                                ResId=reseacher_relation.ResId)
                            res_temp['name'] = reseacher_relation.ResName
                            res_temp['institute'] = resinstitution_temp.InstitutionId.InsName
                            res_temp['avatar'] = reseacher_relation.UserEmail.UserImage
                            res_temp['link'] = reseacher_relation.ResId
                            coopData.append(res_temp)
                        if(coopData.__len__() == 5):
                            donothing = 1
                        else:
                            relationship = Relationship.objects.filter(
                                ResearchId2=resId).all()
                            for i in relationship:
                                if(coopData.__len__() == 5):
                                    break
                                res_temp = {}
                                reseacher_relation = i.ResearchId2
                                resinstitution_temp = ResInstitution.objects.get(
                                    ResId=reseacher_relation.ResId)
                                res_temp['name'] = reseacher_relation.ResName
                                res_temp['institute'] = resinstitution_temp.InstitutionId.InsName
                                res_temp['avatar'] = reseacher_relation.UserEmail.UserImage
                                res_temp['link'] = reseacher_relation.ResId
                                coopData.append(res_temp)

                        res['coopdata'] = coopData
                    except Exception as e:
                        res['coopdata'] = []

                    try:
                        tabledata = []
                        count = 0
                        for i in papersid:
                            try:
                                res_temp = {}
                                res_temp['paperId'] = i.PaperId_id
                                res_temp['title'] = i.PaperId.PaperTitle
                                res_temp['msg'] = i.PaperId.PaperAbstract[:60]
                                res_temp['collectionSum'] = i.PaperId.CollectionNum
                                res_temp['link'] = i.PaperId.PaperUrl
                                res_temp['type'] = '文章'
                                try:
                                    pp = Collection.objects.get(
                                        UserEmail=userId, PaperId=i.PaperId_id)
                                    if(pp is not None):
                                        res_temp['collectStatus'] = True
                                    else:
                                        res_temp['collectStatus'] = False
                                except Exception as e:
                                    res_temp['collectStatus'] = False
                            except Exception as e:
                                continue
                            tabledata.append(res_temp)
                            count = count + 1
                            if(count == 5):
                                break
                        res['tabledata'] = tabledata
                    except Exception as e:
                        res['tabledata'] = []

                    return JsonResponse(res)
                else:
                    return JsonResponse({
                        "status": 2,
                        "message": "请求参数错误"
                    })
            else:
                return JsonResponse({
                    "status": 3,
                    "message": "请求参数错误"
                })
        else:
            return JsonResponse({
                "status": 4,
                "message": "请求方法错误"
            })
    except Exception as e:
        return JsonResponse({
            "status": 5,
            "message": str(e)
        })
