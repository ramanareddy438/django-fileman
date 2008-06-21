var ufile = 1;
var currentE = null;
var temp_string = null;

function preview(path){
    $(".preview > .content > p").html("<img src='"+url_preview+path+"'>");
    $('.block > .content').hide();
    $(".preview > .content").show();
    $(".info > .content").show();
}

function fileClick(name){
    path = pwd+"/"+name;
    $.get(url_geturl+path, {}, onSuccessUrl);
    $(".info > .content").show();
    t = name.substr(-4, 4)
    if(t == ".jpg"){
        preview(path);
    } else if(t == ".gif"){
        preview(path);
    } else if(t == ".png"){
        preview(path);
    }
}

function onSuccessUrl(obj){
    $("#url").val(obj);
    $("#download").hide()
    if (obj!="No access."){
        $("#download > a ").attr("href", obj);
        $("#download").show()
    }
    return 0;
}
$(document).ready(function(){
    $("#filelist > tbody > tr:nth-child(odd)").addClass("odd");
    $("#filelist > tbody > tr > td > .dir").each(function(){
        $(this).dblclick(function(){
            window.location=url_home+pwd+"/"+$(this).text();
        });
    });
    $("#filelist > tbody > tr > td > .file").each(function(){
        $(this).dblclick(function(){
            window.location=url_view+pwd+"/"+$(this).text();
        });
    });

    $('.block > h2').each(function(){ $(this).click(function(){
        $('.block > .content').hide();
        $(this).parent().children(".content").toggle();
    }); });

    $("#filelist > tbody > tr > td > .file").each(function(){
        $(this).attr("onclick", 'fileClick($(this).text())');
    });
    
    $("#download").hide()
});

function addFileFild(){
    ufile = ufile+1;
    $("#addFileFild").before('<p><input type="file" name="ufile'+ufile+'" size="16"></p>');
    return 0;
}

function del(){
    if(confirm("Вы уверены, что хотите удалить отмеченные файлы?")){
        $("#fileListForm").attr("action", url_delete+"?next="+pwd);
        $("#fileListForm").submit();
    }
    return 0;
}

function dest(){
    if(confirm("Внимание! Операция не обратима!\nВы уверены, что хотите уничтожить отмеченные файлы?")){
        $("#fileListForm").attr("action", url_destraction+"?next="+pwd);
        $("#fileListForm").submit();
    }
    return 0;
}

function createDir(){
    name = prompt("Создать дирикторию:", "");
    if (name == false || name == null || name.length == 0) {
        return 0;
    }
    window.location=url_createdir+pwd+"/"+name;
    return 0;
}

function copy_one(element, filename, filepath){
    currentE = $(element).parent();
    $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
    $.post(url_addbufer, {'path': filepath, 'action': "copy"}, successCopy, "json");
    $('.buffer > h2').click();
    return 0;
}

function successCopy(data){
    if(data.status=="success"){
        $("#clearBuffer").hide();
        currentE.html('<img src="'+url_media+'/page_white_copy.png" alt="Копировать">');
        $(".buffer > .content").after(
            '<div><img src="'+url_media+'/page_white_copy.png">'+
            nameFromPath(data.path)+
            ' <a href="#" onclick="return RemoveFromBuffer(this, \''+
            data.path+'\');"><img src="'+url_media+'/cross.png"></a></div>');
    }
    else {
        alert("Произошла ошибка.\nСервер сообщает:\n"+data.msg);
    }
    return 0;
}

function cut_one(element, filename, filepath){
    currentE = $(element).parent();
    temp_string = filepath;
    $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
    $.post(url_addbufer, {'path': filepath, 'action': "cut"}, successCut, "json");
    $('.buffer > h2').click();
    return 0;
}

function successCut(data){
    if(data.status=="success"){
        $("#clearBuffer").hide();
        currentE.html('<img src="'+url_media+'/cut.png" alt="Вырезать">');
        $(".buffer > .content").after(
            '<div><img src="'+url_media+'/cut.png">'+
            nameFromPath(data.path)+
            ' <a href="#" onclick="return RemoveFromBuffer(this, \''+
            data.path+'\');"><img src="'+url_media+'/cross.png"></a></div>');
    }
    else {
        alert("Произошла ошибка.\nСервер сообщает:\n"+data.msg);
    }
    return 0;
}

function rename(element, filename, path){
    currentE = $(element).parent();
    name2 = prompt("Переименовать", filename);
    if (name2 == false || name2 == null || name2.length == 0|| name2 == filename) {
        return 0;
    }
    $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
    $.get(url_home+"../rename/"+path, {'newname': name2}, successRename, "json");
    return 0;
}

function successRename(data){
    if(data.status=="success"){
        currentE.html('<img src="'+url_media+'/pencil.png" alt="Переименовать">');
        $(currentE.parent().children()[0]).children("label").text(data.name)
    }
    else {
        alert("Произошла ошибка.\nСервер сообщает:\n"+data.msg);
    }
    return 0;
}

function del_one(element, filename, filepath){
    currentE = $(element).parent();
    if(confirm("Вы уверены, что хотите удалить "+filename+"?")){
        $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
        $.get(url_delete+filepath, {}, successDelete, "json")
    }
    return 0;
}

function successDelete(data){
    if(data.status=="success"){
        currentE.parent().fadeOut("slow", function(){ 
        currentE.parent().remove();
        $("#filelist > tbody > tr").removeClass("odd");
        $("#filelist > tbody > tr:nth-child(odd)").addClass("odd");
        });
    }
    else {
        alert("При удалении произошла ошибка.\nСервер сообщает:\n"+data.msg);
    }
    return 0;
}

function dest_one(element, filename, filepath){
    currentE = $(element).parent();
    if(confirm("Внимание! Операция не обратима!\nВы уверены, что хотите уничтожить "+filename+"?")){
        $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
        $.get(url_destraction+filepath, {}, successDelete, "json");
    }
    return 0;
}

function RemoveFromBuffer(element, filepath){
    currentE = $(element).parent();
    $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
    $.get(url_removebuffer+filepath, {}, successRemove, "json");
    return 0;
}

function successRemove(data){
    if(data.status=="success"){
        currentE.fadeOut("slow", function(){ 
        currentE.remove();
        });
    }
    else {
        alert("Произошла ошибка.\nСервер сообщает:\n"+data.msg);
    }
    return 0;
}

function nameFromPath(path){
    name = path.split("/");
    name = name[$(name).size()-1];
    return name;
}
