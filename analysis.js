$(document).ready(function(){
	// function DropDown(el) {
	//     this.dd = el;
	//     this.placeholder = this.dd.children('span');
	//     this.opts = this.dd.find('ul.dropdown > li');
	//     this.val = '';
	//     this.index = -1;
	//     this.initEvents();
	// }
	// DropDown.prototype = {
	//     initEvents : function() {
	//         var obj = this;
	 
	//         obj.dd.on('click', function(event){
	//             $(this).toggleClass('active');
	//             return false;
	//         });
	 
	//         obj.opts.on('click',function(){
	//             var opt = $(this);
	//             obj.val = opt.text();
	//             obj.index = opt.index();
	//             obj.placeholder.text(obj.val);

	//             console.log(opt.attr('optionId'));
	//         });
	//     },
	//     getValue : function() {
	//         return this.val;
	//     },
	//     getIndex : function() {
	//         return this.index;
	//     }
	// }
 
  
 //    var dd = new DropDown( $('#dd') );

 	//toggle dropdown
 	$("#dd").on("click", function() {
 		$(this).toggleClass("active");
 	})

 	//when a dropdown element selected, display it and active the appropriate form
 	$('ul.dropdown > li').on("click", function(){
 		$("#ddDisplay").text($(this).text());
 		console.log($(this).attr("value"));
 	})
 
    $(document).click(function(el) {
        // all dropdowns
        if ($(el.target).attr('id') != 'dd') {
	        $('.wrapper-dropdown-3').removeClass('active');
	    }

    });

    // console.log(dd.getValue());
 
});