from django.http import  HttpResponse,JsonResponse
from ResModel.models import Collection
from ResModel.models import HubUser
from ResModel.models import Paper
from ResModel.models import Patent
from ResModel.models import Project

def get_collection(request):
    user_id = request.GET.get('userId')
    user = HubUser.objects.get(UserEmail=user_id)
    c = Collection.objects.filter(UserEmail=user).order_by("-CollectionTime")
    res = list()
    for i in range(0,c.__len__()):
        t = c[i].CollectionType
        if t==1 :
            paper =c[i].PaperId
            j = {
            'paperId': paper.PaperId,
            'title': paper.PaperTitle,
            'msg': paper.PaperAbstract,
            'author': paper.PaperAuthors,
            'type': t,
            'collectionSum':paper.CollectionNum,
            'viewSum':paper.ReadNum,
            'link':paper.PaperUrl,
            'collectTime':c[i].CollectionTime
            }
        elif t==2:
            patent = c[i].PatentId
            j = {
            'paperId': patent.PatentId,
            'title': patent.PatentTitle,
            'msg': patent.PatentAbstract,
            'author': patent.PatentAuthor,
            'type': t,
            'collectionSum':patent.CollectionNum,
            'viewSum':patent.ReadNum,
            'link':patent.PatentUrl,
            'collectTime':c[i].CollectionTime
            }
        elif t==3:
            project = c[i].ProjectId
            j = {
            'paperId': project.ProjectId,
            'title': project.ProjectTitle,
            'msg': project.ProjectAbstract,
            'author': project.ProjectAuthor,
            'type': t,
            'collectionSum':project.CollectionNum,
            'viewSum':project.ReadNum,
            'link':project.PatentUrl,
            'collectTime':c[i].CollectionTime
            }
        res.append(j)
    return JsonResponse({'list' : res})

def add_collection(request):
    user_id = request.GET.get('userId')
    col_id = request.GET.get('paperId')
    col_type = int(request.GET.get('type'))
    succeed = True
    user = HubUser.objects.get(UserEmail=user_id)
    if col_type == 1:
        paper = Paper.objects.get(PaperId=col_id)
        u = Collection(PaperId=paper,UserEmail=user,CollectionType=1)
        u.save()
    elif col_type == 2:
        patent = Patent.objects.get(PatentId=col_id)
        u = Collection(PatentId=patent,UserEmail=user,CollectionType=2)
        u.save()
    elif col_type == 3:
        project = Project.objects.get(ProjectId=col_id)
        u = Collection(ProjectId=project,UserEmail=user,CollectionType=3)
        u.save()
    return JsonResponse({'succeed':succeed})

def del_collection(request):
    user_id = request.GET.get('userId')
    col_id = request.GET.get('paperId')
    col_type = int(request.GET.get('type'))
    succeed = True
    user = HubUser.objects.get(UserEmail=user_id)
    if col_type == 1:
        paper = Paper.objects.get(PaperId=col_id)
        Collection.objects.filter(PaperId=paper,UserEmail=user).delete()
    elif col_type == 2:
        patent = Patent.objects.get(PatentId=col_id)
        Collection.objects.filter(PatentId=patent,UserEmail=user).delete()
    elif col_type == 3:
        project = Paper.objects.get(ProjectId=col_id)
        Collection.objects.filter(PaperId=project,UserEmail=user).delete()
    return JsonResponse({'succeed':succeed})

