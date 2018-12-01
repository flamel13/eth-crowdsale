$('.like-button').on('click', function(e) {
      var t = $(this),
          pid = t.data('pid'),
          req_url = t.data('url');
      t.addClass('liked_photo');

      $.ajax({
          data: {
              photo_id: pid
          },
          url: req_url,
          dataType: 'json',
          type: 'post',
          success: function(data) {
              console.log(data);
          }
      });
  });
