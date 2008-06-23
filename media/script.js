var ufile = 1;
var currentE = null;

// Utils
function nameFromPath(path){
    name = path.split("/");
    name = name[$(name).size()-1];
    return name;
}

// Create items
function copyButton(element, path){
    element.html('<a href="#" ' +
    'onclick="return copy_one(this, \''+nameFromPath(path)+'\', ' +
    '\''+path+'\');" title="'+gettext("Copy")+'">' +
    '<img src="'+url_media+'/page_white_copy.png" ' +
    'alt="'+gettext("Copy")+'"></a>');
    return 0;
}

function cutButton(element, path){
    element.html('<a href="#" ' +
    'onclick="return cut_one(this, \''+nameFromPath(path)+'\', ' +
    '\''+path+'\');" title="'+gettext("Cut")+'">' +
    '<img src="'+url_media+'/cut.png" alt="'+gettext("Cut")+'"></a>');
    return 0;
}

function renameButton(element, path){
    element.html('<a href="#" ' +
    'onclick="return rename(this, \''+nameFromPath(path)+'\', ' +
    '\''+path+'\');" title="'+gettext("Rename")+'">' +
    '<img src="'+url_media+'/pencil.png" alt="'+gettext("Rename")+'"></a>');
    return 0;
}

function deleteButton(element, path){
    element.html('<a href="#" ' +
    'onclick="return del_one(this, \''+nameFromPath(path)+'\', ' +
    '\''+path+'\');" title="'+gettext("Delete")+'">' +
    '<img src="'+url_media+'/delete.png" alt="'+gettext("Delete")+'"></a>');
    return 0;
}

function destButton(element, path){
    element.html('<a href="#" ' +
    'onclick="return dest_one(this, \''+nameFromPath(path)+'\', ' +
    '\''+path+'\');" title="'+gettext("Destroy")+'">' +
    '<img src="'+url_media+'/cross.png" alt="'+gettext("Destroy")+'"></a>');
    return 0;
}

function preview(path){
    $(".preview > .content > p").html("<img src='"+url_preview+path+"'>");
    $('.block > .content').hide();
    $(".preview > .content").show();
    $(".info > .content").show();
}

function addFileFild(){
    ufile = ufile+1;
    $("#addFileFild").before('<p><input type="file" name="ufile'+ufile+'" size="10"></p>');
    return 0;
}

// Events
function fileClick(name){
    path = pwd+"/"+name;
    $.get(url_geturl+path, {}, onSuccessUrl, "json");
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

function del(){
    if(confirm(gettext("Are you sure you want to delete selected files?"))){
        $("#fileListForm").attr("action", url_delete+"?next="+pwd);
        $("#fileListForm").submit();
    }
    return 0;
}

function dest(){
    if(confirm(gettext("Attention! The operation is not reversible! \nAre you sure you want to destroy the marked files?"))){
        $("#fileListForm").attr("action", url_destraction+"?next="+pwd);
        $("#fileListForm").submit();
    }
    return 0;
}

function createDir(){
    name = prompt(gettext("Create directory:"), "");
    if (name == false || name == null || name.length == 0) {
        return 0;
    }
    window.location=url_createdir+pwd+"/"+name;
}

function copy_one(element, filename, filepath){
    currentE = $(element).parent();
    $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
    $.post(url_addbufer, {'path': filepath, 'action': "copy"}, onSuccessCopy, "json");
    $('.buffer > h2').click();
    return 0;
}

function cut_one(element, filename, filepath){
    currentE = $(element).parent();
    $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
    $.post(url_addbufer, {'path': filepath, 'action': "cut"}, onSuccessCut, "json");
    $('.buffer > h2').click();
    return 0;
}

function rename(element, filename, path){
    currentE = $(element).parent();
    name2 = prompt(gettext("Rename"), filename);
    if (name2 == false || name2 == null || name2.length == 0|| name2 == filename) {
        return 0;
    }
    $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
    $.get(url_home+"../rename/"+path, {'newname': name2}, onSuccessRename, "json");
    return 0;
}

function del_one(element, filename, filepath){
    currentE = $(element).parent();
    if(confirm(gettext("Are you sure you want to delete ")+filename+"?")){
        $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
        $.get(url_delete+filepath, {}, onSuccessDelete, "json")
    }
    return 0;
}

function dest_one(element, filename, filepath){
    currentE = $(element).parent();
    if(confirm(gettext("Attention! The operation is not reversible! \nAre you sure you want to destroy ")+filename+"?")){
        $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
        $.get(url_destraction+filepath, {}, onSuccessDelete, "json");
    }
    return 0;
}

function RemoveFromBuffer(element, filepath){
    currentE = $(element).parent();
    $(element).parent().html("<img src='"+url_media+"/ajax-loader.gif'>");
    $.get(url_removebuffer+filepath, {}, onSuccessRemove, "json");
    return 0;
}

// Success ajax
function onSuccessUrl(data){
    if(data.status=="success"){
        $("#url").val(data.url);
        $("#clipboard").removeAttr("disabled");
        $("#clipboard").click(function(){ $.clipboard(data.url); });
        $("#download > a ").attr("href", data.url);
        $("#clipboard").show();
        $("#download").show()
    }
    else {
        $("#url").val(gettext("No access."));
        $("#clipboard").hide(); 
        $("#download").hide()
    }
    return 0;
}

function onSuccessCopy(data){
    if(data.status=="success"){
        $("#clearBuffer").hide();
        copyButton(currentE, data.path);
        $(".buffer > .content").after(
            '<div><img src="'+url_media+'/page_white_copy.png">'+
            nameFromPath(data.path)+
            ' <a href="#" onclick="return RemoveFromBuffer(this, \''+
            data.path+'\');"><img src="'+url_media+'/cross.png"></a></div>');
    }
    else {
        alert(gettext("Error.\nServer reports:\n")+data.msg);
    }
    return 0;
}

function onSuccessCut(data){
    if(data.status=="success"){
        $("#clearBuffer").hide();
        cutButton(currentE, data.path);
        $(".buffer > .content").after(
            '<div><img src="'+url_media+'/cut.png">'+
            nameFromPath(data.path)+
            ' <a href="#" onclick="return RemoveFromBuffer(this, \''+
            data.path+'\');"><img src="'+url_media+'/cross.png"></a></div>');
    }
    else {
        alert(gettext("Error.\nServer reports:\n")+data.msg);
    }
    return 0;
}

function onSuccessRename(data){
    if(data.status=="success"){
        $(currentE.parent().children()[0]).children("label").text(nameFromPath(data.path));
        copyButton(currentE.parent().children(".copy"), data.path);
        cutButton(currentE.parent().children(".cut"), data.path);
        renameButton(currentE, data.path);
        deleteButton(currentE.parent().children(".del"), data.path);
        destButton(currentE.parent().children(".dest"), data.path);
    }
    else {
        alert(gettext("Error.\nServer reports:\n")+data.msg);
    }
    return 0;
}

function onSuccessDelete(data){
    if(data.status=="success"){
        currentE.parent().fadeOut("slow", function(){ 
        currentE.parent().remove();
        $("#filelist > tbody > tr").removeClass("odd");
        $("#filelist > tbody > tr:nth-child(odd)").addClass("odd");
        });
    }
    else {
        alert(gettext("Error.\nServer reports:\n")+data.msg);
    }
    return 0;
}

function onSuccessRemove(data){
    if(data.status=="success"){
        currentE.fadeOut("slow", function(){ 
        currentE.remove();
        });
    }
    else {
        alert(gettext("Error.\nServer reports:\n")+data.msg);
    }
    return 0;
}

// Ready!
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
    
    $("#download").hide();
    $("#clipboard").hide();
    
    $.clipboardReady(function(){}, { swfpath: url_media+"/jquery.clipboard.swf" });
});
