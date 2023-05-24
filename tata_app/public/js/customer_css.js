frappe.ui.form.on('Customer', {

	refresh(frm) {
	    var element = document.querySelectorAll(".form-section")[3];
        element.setAttribute("id","section-no1");
		set_css(frm)
		var user = frappe.session.user_email;

        frappe.call({
			method: "user_number",
			args: { 'user_number': user },
		}).then(records => {
			var num = records["message"];
			// alert(num)
			var agent_number = num	
			frm.add_custom_button(__('Click-To-Call'), function(){
				var phone=frm.doc.phone
				// console.log(phone)
				var whatsapp_no = frm.doc.whatsapp_no;
				// console.log(whatsapp_no)
				var phone_ext = frm.doc.phone_ext;
				console.log(phone_ext)
				var destination_number = frm.doc.mobile;
				console.log(destination_number)
				if(destination_number==null){
					var destination_number=""
				}
				if(phone_ext==null){
					var phone_ext=""
				}
				if(whatsapp_no==null){
					var whatsapp_no=""
				}
				if(phone==null){
					var phone=""
				}
	
					frappe.confirm(
						"Are you sure want To Call?" + "<br><br>" + "<input type='radio' id='1' name='a' value=" + destination_number + "><label for='html'>"+ "Moblie No :- "+destination_number + "</label><br>" + "<input type='radio' id='2' name='a' value=" + phone + "><label for='html'>"+ "Phone No :- " + phone + "</label><br>"+ "<input type='radio' id='3' name='a' value=" + whatsapp_no + "><label for='html'>"+ "Whats-App No :- " + whatsapp_no + "</label><br>"+ "<input type='radio' id='4' name='a' value=" + phone_ext + "><label for='html'>"+ "Phone Ext No :- " + phone_ext + "</label><br>",
		  
				  function(){
					var a1=document.querySelector('input[name="a"]:checked').value;
						console.log(a1)
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
	},
	call3:function(frm){
		var no =frm.doc.phone
		click_call(frm,no)
	},
	call1:function(frm){
		var no =frm.doc.mobile
		console.log(no)
		click_call(frm,no)
	},
	call2:function(frm){
		var no =frm.doc.whatsapp_no 
		click_call(frm,no)
	},
	call4:function(frm){
		var no =frm.doc.phone_ext
		console.log(no)
		click_call(frm,no)
	},
});


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

function connect_to_call(agent_number){
    var a1=document.querySelector('input[name="a"]:checked').value;
						console.log(a1)
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

function set_css(frm){
	// 	console.log("set_css")
		$("#section-no1 button").css("background","#0275d8")
		$("#section-no1 button").css("color","#fff")
		document.querySelectorAll("#section-no1 .frappe-control")[0].style.marginBottom = '-10px';
		document.querySelectorAll("#section-no1 .frappe-control")[0].style.width = '75%';
		document.querySelectorAll("#section-no1 .frappe-control")[1].style.display = 'flex';
	
		document.querySelectorAll("#section-no1 .frappe-control")[2].style.marginBottom = '-10px';
		document.querySelectorAll("#section-no1 .frappe-control")[2].style.width = '75%';
		document.querySelectorAll("#section-no1 .frappe-control")[3].style.display = 'flex';
	
		document.querySelectorAll("#section-no1 .frappe-control")[4].style.marginBottom = '-10px';
		document.querySelectorAll("#section-no1 .frappe-control")[4].style.width = '75%';
		document.querySelectorAll("#section-no1 .frappe-control")[5].style.display = 'flex';
	
		document.querySelectorAll("#section-no1 .frappe-control")[6].style.marginBottom = '-10px';
		document.querySelectorAll("#section-no1 .frappe-control")[6].style.width = '75%';
		document.querySelectorAll("#section-no1 .frappe-control")[7].style.display = 'flex';
		$("#section-no1 .control-input").css("width","80%")	
		$("#section-no1 .control-input").css("float","left")	
		$("#section-no1 .control-input").css("margin-right","20px")	
	// 	console.log("hello end css")
}