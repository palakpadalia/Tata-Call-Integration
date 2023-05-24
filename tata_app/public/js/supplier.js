
frappe.ui.form.on('Supplier', {
    refresh(frm) {
        var element = document.querySelectorAll(".form-section")[2];
        element.setAttribute("id","section-no1");
        
       
		set_css(frm);
        if(frappe.user.has_role("Vendor") != true){
            var user = frappe.session.user_email;
                frappe.call({
                        method: "user_number",
                        args: { 'user_number': user },
                    }).then(records => {
                        var num = records["message"];
                        // alert(num)
                        frm.add_custom_button(__('Click-To-Call'), function(){
                    
                            var agent_number = num
                            // alert(agent_number)
                            var phone=frm.doc.phone_no
                            var destination_number = frm.doc.mobile_number;
                            var whatsapp_no = frm.doc.whatsapp_no;
                            if(destination_number==null){
                                var destination_number=""
                            }
                            if(whatsapp_no==null){
                                var whatsapp_no=""
                            }
                            if(phone==null){
                                var phone=""
                            }
                            frappe.confirm(
                                "Are you sure want To Call?" + "<br><br>" + "<input type='radio' id='1' name='a' value=" + destination_number + "><label for='html'>"+ "Moblie No :- "+destination_number + "</label><br>" + "<input type='radio' id='2' name='a' value=" + phone + "><label for='html'>"+ "Phone No :- " + phone + "</label><br>"+ "<input type='radio' id='3' name='a' value=" + whatsapp_no + "><label for='html'>"+ "Whats-App No :- " + whatsapp_no + "</label><br>",
                  
                            function(){
                                var a1=document.querySelector('input[name="a"]:checked').value;
                                    // console.log(a1)
                                    // alert(a1)
                                    if(a1==""){
                                        frappe.msgprint("you Don't Have Any Number so you can't connect call",'Error')
                                    }
                                    else{
                                        
                                        frappe.call({
                                            
                                            method:"tata_app.api.click_to_call", 
                                            args: {'agent_number':agent_number,'destination_number':a1},
                                            callback: function(r) {
                                                // alert("done")
                                            }
                                        });
                                    }	
                            }
                            )
                        })
        
            
                    })  
            }
                
            },
        call1:function(frm){
            var no =frm.doc.mobile_number
            click_call(frm,no)
        },
        call2:function(frm){
            var no =frm.doc.phone_no
            click_call(frm,no)
        },
        call3:function(frm){
            var no =frm.doc.whatsapp_no
            click_call(frm,no)
        },
    })

function set_css(frm){
    $("#section-no1 button").css("background","#0275d8")
    $("#section-no1 button").css("color","#fff")
    document.querySelectorAll("#section-no1 .frappe-control")[1].style.marginTop = '30px';
    document.querySelectorAll("#section-no1 .frappe-control")[3].style.marginTop = '30px';
    document.querySelectorAll("#section-no1 .frappe-control")[5].style.marginTop = '30px';
}

function click_call(frm,no){
        if(no==null)
        {
            frappe.msgprint("you Don't Have Phone Number so you can't connect call",'Error')		
        }
        else
        {
            var user = frappe.session.user_email;
                frappe.call({
                    method: "user_number",
                    args: { 'user_number': user }
                }).then(records => {
                    var num = records["message"];
                    var agent_number = num	
                            frappe.confirm(
                                "Are you sure want To Call?",				
                            function(){
                            frappe.call({
                                method:"tata_app.api.click_to_call", 
                                args: {'agent_number':agent_number,'destination_number':no},
                                callback: function(r) {
                                }
                            });
                            }
                            )
                        })
            }
}