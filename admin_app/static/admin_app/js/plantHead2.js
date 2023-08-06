(function($) {
    'use strict';

    $(document).ready(function() {

        // function check_requests();

        if (window.location.href == "http://127.0.0.1:8000/project/plantHead/#home") {
            window.location.href = "http://127.0.0.1:8000/project/plantHead/"

        }
        let path = String(window.location.href);
        let pos = path.search('#');
        console.log(path);
        console.log(path.slice(pos + 1));

        if (pos != -1) {
            if (path.slice(pos + 1) == 'home') {
                $('.ph#filter').removeClass('d-none')

            }
            if (path.slice(pos + 1) != 'request') {
                $('.ph#requests').addClass('d-none');
                $('.ph#home').removeClass('d-none');
                $('.ph#home').removeClass('d-none');
                $('.ph#filter').removeClass('d-none')

                $('#ph-sidebar li.nv').removeClass('active')
                $(':not(.nv.request)').addClass('active')
            } else {
                $('.ph#filter').addClass('d-none')
                $('.ph#home').addClass('d-none');
                $('.ph#requests').removeClass('d-none');

                $('#ph-sidebar li.nv').removeClass('active')
                $('#ph-sidebar li.nv.request').addClass('active')
                setInterval(check_requests, 2000)
            }
        }

        $('#ph-sidebar li.nv').click(function() {
            $('#ph-sidebar li.nv').removeClass('active')
            $(this).addClass('active')

            if ($('#ph-sidebar li.nv.request').hasClass('active')) {
                console.log("Request Window");
                $('.ph#home').addClass('d-none');
                $('.ph#filter').addClass('d-none');
                $('.ph#requests').removeClass('d-none');
                setInterval(check_requests, 2000)
            } else {
                console.log("Home Window");
                $('.ph#requests').addClass('d-none');
                $('.ph#home').removeClass('d-none');
                $('.ph#filter').removeClass('d-none');
            }
        });

        const check_requests = () => {
            $.ajax({
                type: "Get",
                url: "requests/",
                success: function(response) {
                    let requests = response.requests;
                    let content = ''
                    requests.forEach(request => {
                        content += `<tr class="">
                          <td>${request['id']}</td>
                        <td>
                          <span class="pl-2">${request['name']}</span>
                          </td>
                          <td>${request['age']}</td>
                          <td>${request['gender']}</td>
                        <td>${request['mobile']}</td>
                        <td>${request['aadhar']}</td>
                        <td>${request['department']}</td>
                        <td>${request['entry_time']}</td>
                        <td></td>
                        
                        <td align="center">
                          <button
                            type="button"
                            class="btn btn-outline-secondary btn-rounded btn-icon btn-exit"
                            >
                            <i class="icofont-tick-mark"></i>
                            </button>
                            </td>
                            <td align="center">
                        <button
                            type="button"
                            class="btn btn-outline-danger btn-rounded btn-icon cancel-req"
                            >
                            <i class="icofont-tick-mark"></i>
                            </button>
                        </td>
                      </tr>`
                    })

                    $('#requests #tbody').html(content)
                        // Cancel request for exit
                    $('.markExit .table button.cancel-req' || '').click(function(e) {
                        let dateTime = new Date()
                        let currentDate = dateTime.getDay() + "/" + dateTime.getMonth() + "/" + dateTime.getFullYear()
                        let currentTime = dateTime.getHours() + ":" + dateTime.getMinutes() + ":" + dateTime.getSeconds()

                        if (confirm("Confirm to cancel the request ?\nDate : " + currentDate + "\nTime : " + currentTime)) {
                            console.log($(this).parents('tr').children().eq(1).text())
                            $.ajax({
                                type: "Get",
                                url: "cancelRequest/",
                                data: {
                                    ids: $(this).parents('tr').children().eq(0).text()
                                },
                                success: function(response) {
                                    if (response.status) {
                                        console.log('Request Cancelled')
                                    } else {
                                        alert('Something went wrong!!!')
                                    }
                                }
                            });
                        }
                    });

                    // Mark single out time of worker
                    $('.markExit .table button.btn-exit').click(function(e) {
                        let dateTime = new Date()
                        let currentDate = dateTime.getDay() + "/" + dateTime.getMonth() + "/" + dateTime.getFullYear()
                        let currentTime = dateTime.getHours() + ":" + dateTime.getMinutes() + ":" + dateTime.getSeconds()

                        if (confirm("Confirm mark out time?\nDate : " + currentDate + "\nTime : " + currentTime)) {
                            console.log($(this).parents('tr').children().eq(1).text())
                            $.ajax({
                                type: "Get",
                                url: "markExit/",
                                data: {
                                    ids: $(this).parents('tr').children().eq(0).text()
                                },
                                success: function(response) {
                                    if (response.status) {
                                        $("#home").prepend('<div class="alert alert-success alert-dismissible fade show" role="alert"> <strong>Message! </strong> Out Time Marked Successfully <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
                                        // console.log($(tr))
                                        // $(tr).addClass('d-none')
                                    } else {
                                        alert('Something went wrong!!!')
                                    }
                                }
                            });
                        }
                    });

                }
            })
        }

        if (location.href == "http://127.0.0.1:8000/project/plantHead/#request") {
            alert()
            console.log(location.href)
            $('#filter').addClass('d-none')
            setInterval(check_requests, 1000)
        }
    })

})(jQuery);