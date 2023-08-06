$(function () {
    init()
}
)
var data=[];
function init() {
        var sjson ={};
    var tags=[]
    $("#myselect").change(function () {
        alert( $("#myselect").val())
    });

    $(".option").bind('DOMAttrModified', function(e) {
        console.log('element now contains: ' + $(e.target).html())

    });
    var cur_selected=$("#id_division").val()

    $.get("/api/subcategory",function (d) {
        // dic = JSON.parse(data);
        data = d.list
        console.log("curl:"+cur_selected)
        console.log(data)
        $("input[name='survey_relate']").removeAttr("required")

        setSelected(cur_selected,true)
        // $("#id_tag_wrap_container")
    })
    $("#id_division").change(function () {
        console.log($("#id_division").val());
        $(".selectize-control .single").css("display","none");
        var product =$(this).val();
        setSelected(product)
    });

}
function  setSelected(product,init=false) {
        var cur_surveys =[]
        $("#id_division_sub").selectize()[0].selectize.clearOptions()
        for (var i=0; i< data.length;i++)
        {
            if (data[i].divisionSub_parent== product)
            {
                cur_surveys.push((data[i].id).toString())
                 var test = {text: data[i].sub_name, value: data[i].id, $order: i + 1};
                $("#id_division_sub").selectize()[0].selectize.addOption(test); //添加数据
            }

        }

        // //二级select清空选项
        // for (var i = 0; i < data.length; i++) {
        //     console.log(data[i]);
        //     var item = data[i];
        //     var test = {text: data[i].name, value: data[i].id, $order: i + 1}; //遍历数据,拼凑出selectize需要的格式
        //
        // }
      // cur_surveys = this.data.filter(item => item.division === $(this).val())

    }