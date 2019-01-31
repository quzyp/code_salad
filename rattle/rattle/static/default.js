$('.widget').on('click input', (function(event) {
   $.post('/',
          {'event' : event.type,
           'id_' : $(this).attr('id'),
            'props' : JSON.stringify(get_props($(this)))},
      function(response){
        json_ = JSON.parse(response);
        for (var k in json_) {
            $('#'+json_[k].id_).prop(json_[k].key, json_[k].value);
        }
   });
}));

function get_props(obj) {
    return {
        'value': obj.val()
    };
}