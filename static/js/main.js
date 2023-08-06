(function($) {
    'use strict';

    $('.eye').click(function(e) {
        // alert(document.getElementById("pass"))
        let eye = document.getElementById('pass')
        if (eye.type == "password") {
            eye.type = 'text'
        } else {
            eye.type = 'password'
        }

        let ele = document.getElementsByClassName('eye icofont-eye')
        console.log(ele)
        $('.eye').toggleClass('icofont-eye icofont-eye-blocked')
    });

    document.onreadystatechange = function() {
        $('.fp-form-box').addClass('d-none')
    }

    $('.fp-group').click(function() {
        $('.fp-form-box').removeClass('d-none')
        $('.login-form-box').addClass('d-none')
        $('.changePass').addClass('d-none')
    })

    $('.back_login').click(function() {
        $('.fp-form-box').addClass('d-none')
        $('.login-form-box').removeClass('d-none')
    })

    let otp;
    $('.fp-verify, #resend').click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "Get",
            url: "verifyOTP/",
            data: {
                email: $('#fp-email').val()
            },
            success: function(response) {
                if (response.status) {
                    otp = response.OTP
                    $('.fp-verify').val("OTP sent...")
                    $('.fp-verify').prop('disabled', true);
                    document.getElementById('otp').disabled = false;
                    document.getElementById('otp').focus();
                    $('#resend').removeClass('d-none')
                    alert('OTP sent...\nEmail Address: ' + response.email)
                } else {
                    alert('Invalid Email address')
                }
            }
        })
    })

    $('#otp').on('input', function() {
        if ($('#otp').val().length >= 6 && $('#otp').val() != otp) {
            alert('Invalid OTP')
        } else if ($('#otp').val() == otp) {
            // alert('valid')
            $('.login-form-box').addClass('d-none')
            $('.verifyOTP').addClass('d-none')
            $('.changePass').removeClass('d-none')
        }
    })

    $('#chngPass').click(function(e) {
        e.preventDefault()
        let email = $('#fp-email').val()
        let pass1 = $('#new-pass').val()
        let pass2 = $('#con-pass').val()

        let re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/

        if (!(re.test(pass1)) || pass1 != pass2) {
            alert('Please check your passwords...')
            $('#new-pass').focus()
        } else {
            if (confirm('Confirm change password?')) {
                $.ajax({
                    type: 'Get',
                    url: 'changePassword',
                    data: {
                        email: email,
                        password: pass1
                    },
                    success: function(response) {
                        if (response.status) {
                            alert('Password changed successfully!!!')
                            window.location.reload()
                        } else {
                            alert('Something went wrong...Try again :(')
                        }
                    }
                })
            } else {
                window.location.reload()
            }
        }
    })

})(jQuery);