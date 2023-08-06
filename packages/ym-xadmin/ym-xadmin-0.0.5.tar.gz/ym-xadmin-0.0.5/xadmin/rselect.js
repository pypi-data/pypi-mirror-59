$(function () {
    init()
}
)
var data=[];
function init() {
        var sjson ={};
    var tags=[]
    $("#id_survey_relate_wrap_container").hide()
    var cur_selected=$("#id_division").val()
    var cur_sub_selected =$("#id_division_sub").val()
    $.get("/api/Surveys",function (d) {
        // dic = JSON.parse(data);
        data = d.list;
        qlist= d.qlist;
        $("input[name='survey_relate']").removeAttr("required")
        $("#id_survey_relate_wrap_container").show()
        setSelected1(cur_selected,true)
        // $("#id_tag_wrap_container")
    })
    $("#id_division").change(function () {
        console.log();
        var product =$(this).val();
        setSelected1(product)
    });
    $("#id_division_sub").change(function () {
        var product =$(this).val();
        setSelected(product)
    })
    function  setSelected1(product,init=false) {
        var cur_surveys =[]

        // $("#id_division_sub").selectize()[0].selectize.clearOptions();
        for (var i=0; i< data.length;i++)
        {
            if (data[i].divisionSub_parent== product)
            {
                cur_surveys.push((data[i].id).toString())
                 var test = {text: data[i].sub_name, value: data[i].id, $order: i + 1};
                $("#id_division_sub").selectize()[0].selectize.addOption(test); //添加数据

            }
            else
            {
                $("#id_division_sub").selectize()[0].selectize.removeOption(data[i].id)
            }

        }

        if(cur_surveys.length==0)
        {
            setDivSelected(product,true)
        }
        else
        {
            if(init==true)
            {
                // $("#id_division_sub").selectize()[0].selectize.setValue(cur_sub_selected, true  );
                setSelected(cur_sub_selected,true)
            }
            else
            {

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
    function setDivSelected(product,init=false) {
         var cur_surveys =[]
        for (var i=0; i< qlist.length;i++)
        {
            if (qlist[i].division__id== product)
            {
                cur_surveys.push((qlist[i].id).toString())
            }

        }
      // cur_surveys = this.data.filter(item => item.division === $(this).val())
       $("#id_survey_relate_wrap_container .checkbox").filter(function(index) {
          return cur_surveys.indexOf($("input",this).val())==-1
          // return $('strong', this).length == 1;
        }).css('display', 'none');
               $("#id_survey_relate_wrap_container .checkbox").filter(function(index) {
          return cur_surveys.indexOf($("input",this).val())==-1
          // return $('strong', this).length == 1;
        }).css('display', '');
         $("#id_survey_relate_wrap_container .checkbox").each(function () {
            if(cur_surveys.indexOf($("input",this).val())==-1)
            {
                $(this).css('display', 'none');
                $("input",this).removeAttr("name")
            }else
            {
                 $(this).css('display', '');
                  $("input",this).attr("name","survey_relate")
            }
            if(!init)
            {
                $("input",this).removeAttr("checked")
            }

         })
    }
function  setSelected(product,init=false) {
        var cur_surveys =[]
        for (var i=0; i< qlist.length;i++)
        {
            if (qlist[i].division_sub__id== product)
            {
                cur_surveys.push((qlist[i].id).toString())
            }

        }
      // cur_surveys = this.data.filter(item => item.division === $(this).val())
       $("#id_survey_relate_wrap_container .checkbox").filter(function(index) {
          return cur_surveys.indexOf($("input",this).val())==-1
          // return $('strong', this).length == 1;
        }).css('display', 'none');
               $("#id_survey_relate_wrap_container .checkbox").filter(function(index) {
          return cur_surveys.indexOf($("input",this).val())==-1
          // return $('strong', this).length == 1;
        }).css('display', '');
         $("#id_survey_relate_wrap_container .checkbox").each(function () {
            if(cur_surveys.indexOf($("input",this).val())==-1)
            {
                $(this).css('display', 'none');
                $("input",this).removeAttr("name")
            }else
            {
                 $(this).css('display', '');
                  $("input",this).attr("name","survey_relate")
            }
            if(!init)
            {
                $("input",this).removeAttr("checked")
            }

         })
    }
}
