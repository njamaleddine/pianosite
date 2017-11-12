'use strict';
$(document).ready(function(){
  var panelArrowIcon = '.product-search-panel-arrow';

  function collapseSearchPanels() {
    if ($(window).width() < 768) {
      $(panelArrowIcon).show();
      $('.search-panel-collapse').collapse('hide');
    } else {
      $(panelArrowIcon).hide();
      $('.search-panel-collapse').collapse('show');
    }
  }

  $(window).on('resize', function(){
    $('.search-panel-collapse').collapse({'toggle': true})
    collapseSearchPanels();
  });
  $('.search-panel-collapse').collapse({'toggle': false})
  collapseSearchPanels();
});
