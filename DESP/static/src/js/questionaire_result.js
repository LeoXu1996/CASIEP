function submit() {
    $('form').each(function () {
        console.log($(this).find('input[name="questiontype"]').val()); //题型
        questionid = $(this).find('input[name="questionid"]').val()
        questioncls = $(this).find('input[name="questionclass"]').val()
        questiontype_sbt = $(this).find('input[name="questiontype"]').val()
        if ($(this).find('input[name="questiontype"]').val() === '选择题') {
            if ($(this).find('input[name="questionclass"]').val() === '单选'){
                $(this).find("input:radio[name='choice']:checked").each(function () {
                console.log($(this).attr('data-index'));//第几个被勾选了 注意是从0开始的
                send_info = $(this).attr('data-index');
                var reg = /[\s\S*][___]+/;
                if (reg.test($(this).next().text()) === true) { //选项中包含填空
                    console.log(reg)
                    var result = ($(this).next().text()).search(reg);
                }

                $.ajax({
                    type: 'post',
                    data: {
                        'send_info': send_info,
                        'questionid': questionid,
                        'questionclass': '单选',
                        'questiontype': questiontype_sbt,
                    },
                    url: "/user/answer_save",
                });
            });
            }else {
                var selectlist = [];
                $(this).find("input:checkbox[name='choice']:checked").each(function () {
                    console.log($(this).attr('data-index'));//第几个被勾选了 注意是从0开始的
                    send_info = $(this).attr('data-index');
                    selectlist.push(send_info)
                    console.log(selectlist)
                    // var reg = /[\s\S*][___]+/;
                    // if (reg.test($(this).next().text()) === true) { //选项中包含填空
                    //     console.log(reg)
                    //     var result = ($(this).next().text()).search(reg);
                    // }
                });

                $.ajax({
                    type: 'post',
                    traditional: true,
                    data: {
                        'send_info': JSON.stringify(selectlist),
                        'questionid': questionid,
                        'questionclass': '多选',
                        'questiontype': questiontype_sbt,
                    },
                    url: "/user/answer_save",
                });
            }
        }
        // $.ajax({
        //     type: 'post',
        //     data: $(this).serialize(),
        //     url: '/user/questionaire_submit',
        //     success: function (data) {
        //         console.log(data);
        //         window.location.reload();
        //     }
        // });
        if ($(this).find('input[name="questiontype"]').val() === '简答题') {
            send_info = $(this).find('textarea[name="answerarea"]').val();
            $.ajax({
                type: 'post',
                data: {
                    'send_info':send_info,
                    'questionid':questionid,
                    'questionclass':'单选',
                    'questiontype': questiontype_sbt,

                },
                url: "/user/answer_save",
                // success: function (data) {
                //     console.log(data);
                //     window.location.reload();
                // }
            });
        }

        if ($(this).find('input[name="questiontype"]').val() === '填空题') {
            var blank_filled = [];
            $(this).find('input[name="ques"]').each(function (){
                send_info = $(this).val();
                console.log(send_info);
                blank_filled.push(send_info);
            })
            $.ajax({
                type: 'post',
                data: {
                    'send_info':JSON.stringify(blank_filled),
                    'questionid':questionid,
                    'questionclass':'单选',
                    'questiontype': questiontype_sbt,

                },
                url: "/user/answer_save",
                // success: function (data) {
                //     console.log(data);
                //     window.location.reload();
                // }
            });
        }

        if ($(this).find('input[name="questiontype"]').val() === '矩阵题') {
            if ($(this).find('input[name="questionclass"]').val() === '单选'){
                $(this).find("input:radio[name='choice']:checked").each(function () {
                console.log($(this).attr('data-index'));//第几个被勾选了 注意是从0开始的
                send_info = $(this).attr('data-index');
                var reg = /[\s\S*][___]+/;
                if (reg.test($(this).next().text()) === true) { //选项中包含填空
                    console.log(reg)
                    var result = ($(this).next().text()).search(reg);
                }

                $.ajax({
                    type: 'post',
                    data: {
                        'send_info': send_info,
                        'questionid': questionid,
                        'questionclass': '单选',
                        'questiontype': questiontype_sbt,
                    },
                    url: "/usr/answer_save",
                });
            });
            }else {
                var selectlist = [];
                var length = $(this).find("input:checkbox[name='choice']:checked").length
                $(this).find("input:checkbox[name='choice']:checked").each(function () {
                    console.log($(this).attr('data-index'));//第几个被勾选了 注意是从0开始的
                    send_info = $(this).attr('data-index');
                    selectlist.push(send_info)
                    console.log(selectlist)
                    // var reg = /[\s\S*][___]+/;
                    // if (reg.test($(this).next().text()) === true) { //选项中包含填空
                    //     console.log(reg)
                    //     var result = ($(this).next().text()).search(reg);
                    // }
                });

                $.ajax({
                    type: 'post',
                    traditional: true,
                    data: {
                        'send_info': JSON.stringify(selectlist),
                        'questionid': questionid,
                        'questionclass': '多选',
                        'questiontype': questiontype_sbt,
                    },
                    url: "/user/answer_save",
                });
            }
        }
    });
    alert('保存成功');
}

function ischecked(event) {
    if ($(event.target).is(':checked')) {
        console.log($(event.target).next().text());
        var reg = /[___]+/;
        if (reg.test($(event.target).next().text()) === true) {
            console.log($(event.target).next().text().match(reg)[0])
        }
    }
}

function fillblank(){
    $('[name="fillblank"]').each(function (){
        str = $(this).text();
        arr = str.split('_');

        arr_blank = []; //找出有内容的index值
        for(var i=0;i<arr.length;i++){
            if(arr[i].length !== 0){
                arr_blank.push(i);
            }
        }
        blank_num = []; //根据index值判断有几个空
        for(var i=0;i<arr_blank.length;i++){
            if(i>0){
                bk = arr_blank[i] - arr_blank[i-1];
                if (bk > 1){
                    blank_num.push(bk)
                }
            }
        }
        //将空置从数组中去掉
        for(var i=0;i<arr.length;i++){
            if(arr[i].length === 0){
                arr.splice(i,1);
                i = i-1;
            }
        }
        $(this).hide();
        for (var i=0; i<arr.length;i++) {
            $(this).next().append(
                "<h5 style=\"display: inline\">" + arr[i] + "</h5>\n"
            );
            if (i<blank_num.length){
                $(this).next().append(
                    "<input type='text' name=\"ques\" data-index ="+ i +">\n"
                );
            }
        }

    });

}