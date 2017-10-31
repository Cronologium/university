$(document).ready(function() {
    $('#do-encryption').click(function() {
        var data = {};
        data['alphabet'] = $('#alphabet').val();
        data['data'] = $('#encryption-data').val();
        data['key'] = $('#encryption-key').val();
        $('#encryption-form input').each(function() {
            if($(this).attr('name') == 'csrfmiddlewaretoken') {
                data[$(this).attr('name')] = $(this).val();
            }
        });
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: '/lab1/belaso/encryption',
            data: data,
            success: function(data) {
                if (data['msg'] == 'success') {
                    $('#encryption-output').text(data['data']);
                    $('#encryption-error').text('No errors.');
                } else {
                    $('#encryption-error').text(data['msg']);
                }
            }
        });
    });
   $('#do-decryption').click(function() {
       var data = {};
       data['alphabet'] = $('#alphabet').val();
       data['data'] = $('#decryption-data').val();
       data['key'] = $('#decryption-key').val();
       $('#decryption-form input').each(function() {
            if($(this).attr('name') == 'csrfmiddlewaretoken') {
                data[$(this).attr('name')] = $(this).val();
            }
        });
       $.ajax({
            dataType: 'json',
            type: 'POST',
            url: '/lab1/belaso/decryption',
            data: data,
            success: function(data) {
                if (data['msg'] == 'success') {
                    $('#decryption-output').text(data['data']);
                    $('#decryption-error').text('No errors.');
                } else {
                    $('#decryption-error').text(data['msg']);
                }
            }
       });
   }); 
});