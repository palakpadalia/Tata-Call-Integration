// console.log("Hello This is Start of Desk file pls Consider it")
document.onreadystatechange = function () {

    
    if (document.readyState == "complete") {
        // console.log("This is inner jQuery")
        // console.log("Hello This is event Listener")
        let user = frappe.session.user
        
        frappe.call({
            method: "tata_app.api.login1", 
            args:{
                "user": user,
            }
            }).then(records => {
                
                var role = records["role"]
                var host_name = window.location.origin
                // var supplier_name = records["supplier"]
                if (role=="Vendor"){
                    let navbar = document.querySelector(".navbar-collapse")

                    let report = document.createElement('a')
                    report.href=host_name+"/app/query-report/Compliance%20Report"
                    report.innerText = "Compliance Report"
                    $(report).html(`<i class = "fa fa-file-text-o"></i> Compliance Report`)
                    $(report).addClass("nav-link");
                    navbar.prepend(report)
                    
                    let equipment = document.createElement('a')
                    equipment.href=host_name + "/app/item"
                    equipment.innerText = "Equipment"
                    $(equipment).html(`<i class = "fa fa-truck"></i> Equipments`)
                    $(equipment).addClass("nav-link");
                    navbar.prepend(equipment)

                    let dashboard = document.createElement('a')
                    dashboard.href=host_name+"/app/equipment"
                    dashboard.innerText = "Dashboard"
                    $(dashboard).html(`<i class = "fa fa-desktop"></i> Dashboard`)
                    $(dashboard).addClass("nav-link");
                    navbar.prepend(dashboard)


                    $('#navbar-breadcrumbs').removeClass('d-sm-flex');
                    $('.page-actions').remove();
                    
                }
                else{
                    // alert("Nanananananannaanaaa")
                }
        })
    }
}
// console.log("Hello This is End of Desk file pls Consider it")