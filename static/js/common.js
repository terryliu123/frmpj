function tojsontree(data){
    var jsondata = data;
    var topArr = []; //声明一个数组，存储所有的json数据
            for (var i = 0; i< jsondata.length; i++) {
                if (jsondata[i].parent == 0) {
                    jsondata[i].children = []; //给一级菜单下面添加data数据，存放二级菜单
                    topArr.push(jsondata[i]);  //得到一级菜单
                }
            }

            for (var j = 0; j < topArr.length; j++) {
               for (var i = 0; i < jsondata.length; i++) {
                   if (jsondata[i].parent == topArr[j].id) {
                       jsondata[i].children = [];
                       topArr[j].children.push(jsondata[i]);  //把获取的二级菜单存放到一级菜单的data对象中
                   }
               }
           }

            for (var j = 0; j < topArr.length; j++) {
                for (var m = 0; m < topArr[j].children.length; m++) {
                    for (var i = 0; i < jsondata.length; i++) {
                        if (jsondata[i].parent == topArr[j].children[m].id)    {
                           topArr[j].children[m].children.push(jsondata[i]); //把获取的三级菜单存放到二级菜单的data对象中
                        }
                    }
                }
            }
            return topArr;
}