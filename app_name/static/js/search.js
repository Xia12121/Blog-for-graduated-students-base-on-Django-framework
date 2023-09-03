$(document).ready(function() {
    $("#search-button").click(function(event) {
      event.preventDefault();
  
      var searchType = $("#search-select").val();
      var searchKeyword = $("#search-query").val();
    if(searchType==="Ielts score"){
        var url = "http://localhost:8123/ClosestCases_ielts/?ielts_score=" + searchKeyword;
    }
      
    if(searchType==="GPA"){
        var url = "http://localhost:8123/closest_cases_GPA/?gpa=" + searchKeyword;
    }

    if(searchType==="GRE score"){
        var url = "http://localhost:8123/closest_cases_GRE/?gre_score=" + searchKeyword;
    }

      $.get(url, function(data) {
        $(".post-area").empty();
  
        // 创建一个表格来存放每个case对象
        var table = $("<table>").addClass("case-table");
  
        $.each(data, function(index, caseObj) {
          // 创建一个tr用于存放当前对象的所有元素
          var row = $("<tr>").addClass("case-row");
  
          // 输出每个元素到表格中的对应单元格中
          var cellCount = 0;
          for (var key in caseObj) {
            if (caseObj.hasOwnProperty(key)) {
              var cell = $("<td>").addClass("case-cell");
              var elementLabel = $("<span>").addClass("case-label").text(key + ": ");
              var elementValue = $("<span>").addClass("case-value").text(caseObj[key]);
              cell.append(elementLabel).append(elementValue);
              row.append(cell);
              cellCount++;
  
              // 当cellCount等于4时，创建一个新的行，并将cellCount重置为0
              if (cellCount === 4) {
                table.append(row);
                row = $("<tr>").addClass("case-row");
                cellCount = 0;
              }
            }
          }
  
          // 将当前对象的行添加到表格中
          table.append(row);
  
          // 添加一条黑色线条作为分隔符，仅在搜索结果之间添加
          if (index !== data.length - 1) {
            table.append($("<tr>").addClass("separator-row").append($("<td>").attr("colspan", 8)));
            // 跳过分隔符行
            table.append($("<tr>").addClass("empty-row").css("height", "0"));
          }
        });
  
        // 将表格添加到.post-area中
        $(".post-area").append(table);
      });
    });
  });
  