(function($) {
    'use strict';


    function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    $(window).on('load', function() {
        $(document).ready(function() {

            let path = String(window.location.href);
            let pos = path.search('#');
            console.log(path);
            console.log(path.slice(pos + 1));
            if (pos != -1) {
                if (path.slice(pos + 1) != 'latestEntries') {
                    $('.sup#latestEntries').addClass('d-none');
                    $('.sup#home').removeClass('d-none');
                    $('.sup#home').removeClass('d-none');

                    $('#sup-sidebar li.nv').removeClass('active')
                    $(':not(.nv.request)').addClass('active')
                } else {
                    $('.sup#home').addClass('d-none');
                    $('.sup#latestEntries').removeClass('d-none');

                    $('#sup-sidebar li.nv').removeClass('active')
                    $('#sup-sidebar li.nv.request').addClass('active')
                }
            }
        });

        $(document).ready(function() {
            // Initiate AOS
            AOS.init();
        });

        $(document).ready(function() {

            $('#SForm .dropdown,#SUForm .dropdown').click(function() {
                $('#SForm .dropdown,#SUForm .dropdown').toggleClass('show');
                $('#SForm .dropdown .dropdown-menu,#SUForm .dropdown .dropdown-menu').toggleClass('show');
            })

            $('#SForm .dropdown li,#SUForm .dropdown li').click(function() {
                $('#SForm #department,#SUForm #department').val($(this)[0].innerText);
            })

            // changing active nav item of admin page
            $('.sidebar-menu li').click(function() {
                $('.sidebar-menu li').removeClass('active')
                $(this).addClass('active')

                if ($('.sidebar-menu li:eq(2)').hasClass('active')) {
                    console.log("Request Window");
                    $('#department').removeClass('d-none')
                    $('#admin-home').addClass('d-none')
                    $('#header .add-new-user').addClass('d-none')
                    $('#header .add-new-dept').removeClass('d-none')


                } else {
                    console.log("Home Window");
                    $('#admin-home').removeClass('d-none')
                    $('#department').addClass('d-none')
                    $('#header .add-new-user').removeClass('d-none')
                    $('#header .add-new-dept').addClass('d-none')


                }
            });
            // changing active nav item of supervisor page
            $('#sup-sidebar li.nv').click(function() {
                $('#sup-sidebar li.nv').removeClass('active')
                $(this).addClass('active')

                if ($('#sup-sidebar li.nv.request').hasClass('active')) {
                    console.log("Request Window");
                    $('.sup#home').addClass('d-none');
                    setInterval(check_latestEntries, 1000)
                    $('.sup#latestEntries').removeClass('d-none');
                } else {
                    console.log("Home Window");
                    $('.sup#latestEntries').addClass('d-none');
                    $('.sup#home').removeClass('d-none');

                }
            });
        });
    });


    //Add New Department Button
    $('#header .add-new-dept').click(function(e) {
        e.preventDefault();
        $('.overlay-dept-form').removeClass('d-none');
    });

    //Add New User Button
    $('#header .add-new-user').click(function(e) {
        e.preventDefault();
        $('.overlay-form').removeClass('d-none');
    });


    //Choices to add users 
    $('.choices button.pm').click(function(e) {
        e.preventDefault();
        $('.choices').addClass('d-none');
        $('.pm-form').removeClass('d-none');
    });

    $('.choices button.sv').click(function(e) {
        e.preventDefault();
        $('.choices').addClass('d-none');
        $('.sv-form').removeClass('d-none');
    });

    $('.choices button.sc').click(function(e) {
        e.preventDefault();
        $('.choices').addClass('d-none');
        $('.sc-form').removeClass('d-none');
    });

    $('.choices button.cancel').click(function(e) {
        e.preventDefault();
        $('.overlay-form').addClass('d-none');
        $('.choices').removeClass('d-none');
        $('.sv-form').addClass('d-none');
        $('.pm-form').addClass('d-none');
        $('.sc-form').addClass('d-none');
    });


    $('.pm-form button.btn-dark').click(function(e) {
        e.preventDefault();
        $('.choices').removeClass('d-none');
        $('.sv-form').addClass('d-none');
        $('.pm-form').addClass('d-none');
        $('.sc-form').addClass('d-none');
    });

    $('.sv-form button.btn-dark').click(function(e) {
        e.preventDefault();
        $('.choices').removeClass('d-none');
        $('.sv-form').addClass('d-none');
        $('.pm-form').addClass('d-none');
        $('.sc-form').addClass('d-none');
    });

    $('.sc-form button.btn-dark').click(function(e) {
        e.preventDefault();
        $('.choices').removeClass('d-none');
        $('.sv-form').addClass('d-none');
        $('.pm-form').addClass('d-none');
        $('.sc-form').addClass('d-none');
    });

    $('button.edit-form').click(function(e) {
        let text = $(this).parents('.table-responsive').siblings('.card-title').text();

        if (text.toLowerCase() == 'plant head') {

            $('.overlay-update-form').removeClass('d-none');
            $('.sv-update-form').addClass('d-none');
            $('.sc-update-form').addClass('d-none');
            $('.pm-update-form').removeClass('d-none');

            document.forms['PHUForm']['id'].value = $(this).parents('tr').children().first().text().trim();
            document.forms['PHUForm']['name'].value = $(this).parents('tr').children().eq(1).text().trim();
            document.forms['PHUForm']['gender'].value = $(this).parents('tr').children().eq(2).text().trim();
            document.forms['PHUForm']['mobile'].value = $(this).parents('tr').children().eq(3).text().trim();
            document.forms['PHUForm']['email'].value = $(this).parents('tr').children().eq(4).text().trim();

        } else if (text.toLowerCase() == 'supervisor') {

            $('.overlay-update-form').removeClass('d-none');
            $('.pm-update-form').addClass('d-none');
            $('.sv-update-form').removeClass('d-none');
            $('.sc-update-form').addClass('d-none');
            document.forms['SUForm']['id'].value = $(this).parents('tr').children().first().text().trim();
            document.forms['SUForm']['name'].value = $(this).parents('tr').children().eq(1).text().trim();
            document.forms['SUForm']['gender'].value = $(this).parents('tr').children().eq(2).text().trim();
            document.forms['SUForm']['mobile'].value = $(this).parents('tr').children().eq(3).text().trim();
            document.forms['SUForm']['email'].value = $(this).parents('tr').children().eq(4).text().trim();
            document.forms['SUForm']['department'].value = $(this).parents('tr').children().eq(5).text().trim();

        } else if (text.toLowerCase() == 'security') {

            $('.overlay-update-form').removeClass('d-none');
            $('.pm-update-form').addClass('d-none');
            $('.sv-update-form').addClass('d-none');
            $('.sc-update-form').removeClass('d-none');
            document.forms['SCUForm']['id'].value = $(this).parents('tr').children().first().text().trim();
            document.forms['SCUForm']['name'].value = $(this).parents('tr').children().eq(1).text().trim();
            document.forms['SCUForm']['gender'].value = $(this).parents('tr').children().eq(2).text().trim();
            document.forms['SCUForm']['mobile'].value = $(this).parents('tr').children().eq(3).text().trim();
            document.forms['SCUForm']['email'].value = $(this).parents('tr').children().eq(4).text().trim();

        }
    });

    $('.overlay-update-form button.btn-dark').click(function(e) {
        e.preventDefault();
        $('.overlay-update-form').addClass('d-none');
    });


    // To delete user
    $('button.delete-user').click(function(e) {
        e.preventDefault();
        $('.overlay-delete-user').removeClass('d-none');
        document.forms['DUForm']['id'].value = $(this).parents('tr').children().first().text().trim();
        document.forms['DUForm']['designation'].value = $(this).parents('.table-responsive').siblings('.card-title').text().trim().toLowerCase();
    });

    $('.choices-delete button.confirm-delete').click(function(e) {
        e.preventDefault();
        $('.overlay-delete-user').addClass('d-none');
        document.forms['DUForm'].submit();
    });

    $('.choices-delete button.cancel-delete').click(function(e) {
        e.preventDefault();
        $('.overlay-delete-user').addClass('d-none');
    });


    // To add new department
    $('#department form .add-dept-btn').click(function(e) {
        e.preventDefault()
        if (confirm('Confirm add new department\nDepartment name : ' + $('#department form #dept-name').val())) {
            document.forms['ADForm']['deptName'].value = $('#department form #dept-name').val().trim();
            document.forms['ADForm'].submit();
        }
    })

    // To cancel adding new department
    $('#department form .cancel-dept-btn').click(function(e) {
        e.preventDefault();
        $('#department form').trigger('reset')
        $('.overlay-dept-form').addClass('d-none');
    });

    // To delete department
    $('button.delete-dept').click(function(e) {
        e.preventDefault();
        $('.overlay-delete-dept').removeClass('d-none');
        document.forms['DDForm']['deptName'].value = $(this).parents('tr').children().first().text().trim();
        console.log($('.overlay-delete-dept .card-body h5 strong'))
        $('.overlay-delete-dept .card-body h4 strong').text($(this).parents('tr').children().eq(1).text().trim());
    });

    $('.overlay-delete-dept button.confirm-delete').click(function(e) {
        e.preventDefault();
        $('.overlay-delete-dept').addClass('d-none');
        document.forms['DDForm'].submit();
    });

    $('.overlay-delete-dept button.cancel-delete').click(function(e) {
        e.preventDefault();
        $('.overlay-delete-dept').addClass('d-none');
    });

    // To search worker by id to mark department entry
    $('.searchButton').click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "Get",
            url: "",
            data: {
                s: $('.searchTerm').val()
            },
            success: function(response) {
                if (response.status) {
                    let info = response.data;
                    document.getElementById('WForm').elements[1].value = info.id;
                    document.getElementById('WForm').elements[2].value = info.w_id;
                    document.getElementById('WForm').elements[3].value = info.name;
                    document.getElementById('WForm').elements[4].value = info.age;

                    let index = 0;
                    if (info.gender == 'Male')
                        index = 0;
                    else
                        index = 1;

                    document.getElementById('WForm').elements[5].selectedIndex = index;
                    document.getElementById('WForm').elements[6].value = info.mobile;
                    document.getElementById('WForm').elements[7].value = info.aadhar;
                    document.getElementById('WForm').elements[5].setAttribute('disabled', true);
                    $('.pm-form #WForm button').removeClass('d-none');
                } else {
                    $('.pm-form #WForm button').addClass('d-none');
                    document.getElementById('WForm').reset();
                    alert("No record found");
                }
            }
        });
    });


    // Supervisor mark entry and exit 
    $('.main-sidebar .sidebar .sidebar-menu .entry').click(function(e) {
        $('.main-sidebar .sidebar-menu .entry').css({
            'background-color': '#00d25b',
            'color': '#fff'
        })

        $('.main-sidebar .sidebar-menu .exit').css({
            'color': '#0090e7',
            'border-color': '#0090e7',
            'background-color': 'transparent'
        })

        $('#home h2').text('Mark In Time')
        $('.markEntry').removeClass('d-none')
        $('.markExit').addClass('d-none')
    });

    $('.main-sidebar .sidebar .sidebar-menu .exit').click(function(e) {
        $('.main-sidebar .sidebar-menu .exit').css({
            'background-color': '#0090e7',
            'color': '#fff'
        })

        $('.main-sidebar .sidebar-menu .entry').css({
            'color': '#00d25b',
            'border-color': '#00d25b',
            'background-color': 'transparent'
        })
        $('#home h2').text('Mark Out Time')
        $('.markEntry').addClass('d-none')
        $('.markExit').removeClass('d-none')
    });

    // $('#home button').click(function(e) {
    //     $('#home .alert').addClass('d-none')
    // });

    $('.form-check-input').click(function(e) {
        if ($('.form-check-input').is(':checked')) {
            $('.markSelected').removeClass('d-none')
        }
        if ($('.form-check-input:checked').length == 0) {
            $('.markSelected').addClass('d-none')
        }
    })


    // Request Plant Head for Exit of the Worker
    $('.markExit .table button.btn-req' || '').click(function(e) {
        let dateTime = new Date()
        let currentDate = dateTime.getDay() + "/" + dateTime.getMonth() + "/" + dateTime.getFullYear()
        let currentTime = dateTime.getHours() + ":" + dateTime.getMinutes() + ":" + dateTime.getSeconds()

        if (confirm("Confirm Request Plant Head for Exit?\nDate : " + currentDate + "\nTime : " + currentTime)) {
            console.log('Hi');
            console.log($(this).parents('tr').children().eq(1).text());
            $.ajax({
                type: "GET",
                url: "requestExit/",
                data: {
                    ids: $(this).parents('tr').children().eq(1).text()
                },
                success: function(response) {
                    if (response.status) {
                        console.log('Request Sent')
                    } else {
                        alert('Something went wrong!!!')
                    }
                }
            });
        }
    });

    // Mark single out time of worker
    $('#markExit .table button.btn-exit').click(function(e) {
        let dateTime = new Date()
        let currentDate = dateTime.getDay() + "/" + dateTime.getMonth() + "/" + dateTime.getFullYear()
        let currentTime = dateTime.getHours() + ":" + dateTime.getMinutes() + ":" + dateTime.getSeconds()

        let tr = $(this).parents('tr')
        console.log()

        if (confirm("Confirm mark out time?\nDate : " + currentDate + "\nTime : " + currentTime)) {
            console.log($(this).parents('tr').children().eq(1).text())
            $.ajax({
                type: "Get",
                url: "markExit/",
                data: {
                    ids: $(this).parents('tr').children().eq(1).text()
                },
                success: function(response) {
                    if (response.status) {
                        tr.addClass('d-none')
                        $("#home").prepend('<div class="alert alert-success alert-dismissible fade show" role="alert"> <strong>Message! </strong> Out Time Marked Successfully <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');

                    } else {
                        alert('Something went wrong!!!')
                    }
                }
            });
        }
    });

    // Mark out time of multiple workers at a time
    $('.markExit .markSelected').click(function(e) {
            let dateTime = new Date()
            let currentDate = dateTime.getDay() + "/" + dateTime.getMonth() + "/" + dateTime.getFullYear()
            let currentTime = dateTime.getHours() + ":" + dateTime.getMinutes() + ":" + dateTime.getSeconds()
            if (confirm("Confirm mark out time?\nDate : " + currentDate + "\nTime : " + currentTime)) {
                let checkboxes = document.querySelectorAll(('input[type="checkbox"]:checked'));
                const _ids = []
                for (let checkbox of checkboxes) {
                    _ids[_ids.length] = checkbox.value
                }
                $.ajax({
                    type: "Get",
                    url: "markExit/",
                    data: {
                        ids: _ids.toString()
                    },
                    success: function(response) {
                        if (response.status) {
                            $("#home").prepend('<div class="alert alert-success alert-dismissible fade show" role="alert"> <strong>Message! </strong> Out Time Marked Successfully <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
                            for (var checkbox of checkboxes) {
                                console.log($(checkbox).parents('tr'))
                                $(checkbox).parents('tr').addClass('d-none')
                                $('.markSelected').addClass('d-none')
                            }
                        } else {
                            alert('Something went wrong!!!')
                        }
                    }
                })
            }
        })
        // alert($.cookie("id"));

    $('#filter .id').val(getCookie('id'))

    $('#filter .id').on("input", function() {
        document.cookie = "id = " + $('#filter .id').val()
    })

    $('#filter #customDate').on("input", function() {
        document.cookie = "id = " + $('#filter .id').val()
        document.cookie = "type = date";
        document.cookie = "value = " + $('#filter #customDate').val();
    })

    $('#filter #customWeek').on("input", function() {
        document.cookie = "id = " + $('#filter .id').val()
        document.cookie = "type = week";
        console.log($('#filter #customWeek').val())
        console.log(typeof($('#filter #customWeek').val()))
        document.cookie = "value = " + $('#filter #customWeek').val();
    })

    $('#filter #customMonth').on("input", function() {
        document.cookie = "id = " + $('#filter .id').val()
        document.cookie = "type = month";
        document.cookie = "value = " + $('#filter #customMonth').val();
    })

    $("#filter .applyFilter").click(function(e) {

        window.location.reload()

    })


    $("#filter .removeFilter").click(function(e) {
        document.cookie = "id="
        document.cookie = "value="
        document.cookie = "type="
        window.location.reload()

    })


    const check_latestEntries = () => {
        $.ajax({
            type: "Get",
            url: "latestEntries/",
            success: function(response) {
                let latestEntries = response.latestEntries;
                let content = ''
                latestEntries.forEach(entries => {
                    content += `<tr class="">
                        <td>${entries['id']}</td>
                        <td>
                          <span class="pl-2">${entries['name']}</span>
                        </td>
                        <td>${entries['age']}</td>
                        <td>${entries['gender']}</td>
                        <td>${entries['mobile']}</td>
                        <td>${entries['aadhar']}</td>
                        <td>${entries['entry_time']}</td>
                        <td></td>

                        
                      </tr>`
                })

                $('#latestEntries #tbody').html(content)

            }
        })
    }

    $('.sidebar .latestEntries').click(function() {
        check_latestEntries()
    })
    if (location.href == "http://127.0.0.1:8000/project/supervisor/#latestEntries") {
        setInterval(check_latestEntries, 1000)

    }

})(jQuery);


// To show digital clock in security and supervisor dashboard
function showTime() {
    let date = new Date();
    let h = date.getHours();
    let m = date.getMinutes();
    let s = date.getSeconds();
    let session = "AM";

    if (h == 0) {
        h = 12;
    }

    if (h > 12) {
        h = h - 12;
        session = "PM";
    }

    h = (h < 10) ? "0" + h : h;
    m = (m < 10) ? "0" + m : m;
    s = (s < 10) ? "0" + s : s;

    let time = h + ":" + m + ":" + s + " " + session;
    document.getElementById("MyClockDisplay").textContent = time;

    setTimeout(showTime, 1000);
}
showTime()