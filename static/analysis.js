$(document).ready(function(){
  var averagescoreMap;

 	//toggle dropdown
 	$(".dropdown-toggle").on("click", function() {
 		$(this).toggleClass("active");
 	})

 	//when a dropdown element selected, display it and active the appropriate form
 	$('ul.dropdown > li').on("click", function(){
 		$("#ddDisplay").text($(this).text());
    $("#id_role").val($(this).text());
 	})
 
    $(document).click(function(el) {
        // all dropdowns
        if (!$(el.target).hasClass("dropdown-toggle")) {
	        $('.wrapper-dropdown-3').removeClass('active');
	    }

    });


    //load csv
   $.ajax({
   		url: "authorscore",
	    // var allTextLines = allText.split("\n");
	    // var headers = allTextLines[0].split(',');
	    // var lines = [];
    	// console.log(allTextLines)
	    // for (var i=1; i<allTextLines.length; i++) {
	    //     var data = allTextLines[i].split(',');
	    //     if (data.length == headers.length) {

	    //         var tarr = [];
	    //         for (var j=0; j<headers.length; j++) {
	    //             tarr.push(headers[j]+":"+data[j]);
	    //         }
	    //         lines.push(tarr);
	    //     }
	    // }
	    success: function (data) {

        var authors = [];   
        var json = $.parseJSON(data); 
        for (var key in json) {
          if (json.hasOwnProperty(key)) {
            authors.push(key);
          }
        }
        console.log(authors)
        setAutoComplete(authors);
        averagescoreMap = json;
	    // var lines = $.csv.toArrays(allText);
		}
	}); 

   function setAutoComplete (authors) {
      $( "#name_id" ).autocomplete({
        source: authors
      });
   }  

    $("form").submit(function(event) {
      event.preventDefault();
      var author = $("#name_id").val();
      var score = averagescoreMap[author];
      $("#averagescore_id").val(score);
      console.log($("form").serialize());

      $.ajax({
        url: "/get_money",
        data: $("form").serialize(),
        success: function(data) {
          $(".amount").text(data);
        }
      });
    })




});