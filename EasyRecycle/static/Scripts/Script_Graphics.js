Apex.grid = {
  padding: {
    right: 0,
    left: 0
  }
}

Apex.dataLabels = {
  enabled: false
}

var randomizeArray = function (arg) {
  var array = arg.slice();
  var currentIndex = array.length, temporaryValue, randomIndex;

  while (0 !== currentIndex) {

    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

// data for the sparklines that appear below header area
var sparklineData = [47, 45, 54, 38, 56, 24, 65, 31, 37, 39, 62, 51, 35, 41, 35, 27, 93, 53, 61, 27, 54, 43, 19, 46];

// the default colorPalette for this dashboard
//var colorPalette = ['#01BFD6', '#5564BE', '#F7A600', '#EDCD24', '#F74F58'];
var colorPalette = ['#00D8B6','#008FFB',  '#FEB019', '#FF4560', '#775DD0']

fetch('/first_recycle')
  .then(res => res.json())
  .then(data => {
    const spark1 = {
      chart: {
        id: 'sparkline1',
        group: 'sparklines',
        type: 'area',
        height: 160,
        sparkline: {
          enabled: true
        }
      },
      stroke: {
        curve: 'straight'
      },
      fill: {
        opacity: 1
      },
      series: [{
        name: 'Reciclagem (Kg)',
        data: data.labels.map((date, index) => ({
          x: date,
          y: data.series[index]
        }))
      }],
      xaxis: {
        type: 'datetime'
      },
      colors: [data.color],
      title: {
        text: `${data.total} Kg`,
        offsetX: 30,
        style: {
          fontSize: '24px',
          color: [data.color]
        }
      },
      subtitle: {
        text: data.category,
        offsetX: 30,
        style: {
          fontSize: '14px',
          color: [data.color]
        }
      }
    };

    new ApexCharts(document.querySelector("#spark1"), spark1).render();
  });

  fetch('/second_recycle')
  .then(res => res.json())
  .then(data => {
    const spark2 = {
      chart: {
        id: 'sparkline2',
        group: 'sparklines',
        type: 'area',
        height: 160,
        sparkline: {
          enabled: true
        }
      },
      stroke: {
        curve: 'straight'
      },
      fill: {
        opacity: 1
      },
      series: [{
        name: 'Reciclagem (Kg)',
        data: data.labels.map((date, index) => ({
          x: date,
          y: data.series[index]
        }))
      }],
      xaxis: {
        type: 'datetime'
      },
      colors: [data.color],
      title: {
        text: `${data.total} Kg`,
        offsetX: 30,
        style: {
          fontSize: '24px',
          color: [data.color]
        }
      },
      subtitle: {
        text: data.category,
        offsetX: 30,
        style: {
          fontSize: '14px',
          color: [data.color]
        }
      }
    };

    new ApexCharts(document.querySelector("#spark2"), spark2).render();
  });

  fetch('/third_recycle')
  .then(res => res.json())
  .then(data => {
    const spark3 = {
      chart: {
        id: 'sparkline3',
        group: 'sparklines',
        type: 'area',
        height: 160,
        sparkline: {
          enabled: true
        }
      },
      stroke: {
        curve: 'straight'
      },
      fill: {
        opacity: 1
      },
      series: [{
        name: 'Reciclagem (Kg)',
        data: data.labels.map((date, index) => ({
          x: date,
          y: data.series[index]
        }))
      }],
      xaxis: {
        type: 'datetime'
      },
      colors: [data.color],
      title: {
        text: `${data.total} Kg`,
        offsetX: 30,
        style: {
          fontSize: '24px',
          color: [data.color]
        }
      },
      subtitle: {
        text: data.category,
        offsetX: 30,
        style: {
          fontSize: '14px',
          color: [data.color]
        }
      }
    };

    new ApexCharts(document.querySelector("#spark3"), spark3).render();
  });






  fetch('/peso_por_categoria_data')
  .then(res => res.json())
  .then(data => {
    const optionsBar = {
      chart: {
        type: 'bar',
        height: 380,
        width: '100%',
        stacked: true,
      },
      plotOptions: {
        bar: {
          columnWidth: '45%',
        }
      },
      colors: data.colors,
      series: data.series, // ← series recebidas do backend
      xaxis: {
        categories: data.labels, // ← datas como labels do eixo x
        labels: {
          style: {
            colors: '#78909c'
          }
        },
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        },
      },
      yaxis: {
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        },
        labels: {
          style: {
            colors: '#78909c'
          }
        }
      },
      title: {
        text: 'Reciclagens por dia',
        align: 'left',
        style: {
          fontSize: '18px'
        }
      }
    };

    const chart = new ApexCharts(document.querySelector("#bar"), optionsBar);
    chart.render();
  })
  .catch(err => console.error("Erro ao carregar dados do gráfico:", err));



  fetch('/recycle_by_category')
  .then(res => res.json())
  .then(data => {
    console.log(data);
    var optionDonut = {
      chart: {
        type: 'donut',
        width: '100%',
        height: 400
      },
      dataLabels: { enabled: false },
      plotOptions: {
        pie: {
          customScale: 0.8,
          donut: { size: '75%' },
          offsetY: 20
        }
      },
      colors: data.colors, // ← cores dinâmicas do backend
      title: {
        text: 'Materiais reciclados (Kg)',
        style: { fontSize: '18px' }
      },
      labels: data.labels,
      series: data.series,
      legend: {
        position: 'left',
        offsetY: 80
      }
    };

    var chart = new ApexCharts(document.querySelector("#donut"), optionDonut);
    chart.render();
  });



function trigoSeries(cnt, strength) {
  var data = [];
  for (var i = 0; i < cnt; i++) {
      data.push((Math.sin(i / strength) * (i / strength) + i / strength+1) * (strength*2));
  }

  return data;
}



var optionsLine = {
  chart: {
    height: 340,
    type: 'line',
    zoom: {
      enabled: false
    }
  },
  plotOptions: {
    stroke: {
      width: 4,
      curve: 'smooth'
    },
  },
  colors: colorPalette
  
}

var chartLine = new ApexCharts(document.querySelector('#line'), optionsLine);

// a small hack to extend height in website sample dashboard
chartLine.render().then(function () {
  var ifr = document.querySelector("#wrapper");
  if (ifr.contentDocument) {
    ifr.style.height = ifr.contentDocument.body.scrollHeight + 20 + 'px';
  }
});


// on smaller screen, change the legends position for donut
var mobileDonut = function() {
  if($(window).width() < 768) {
    donut.updateOptions({
      plotOptions: {
        pie: {
          offsetY: -15,
        }
      },
      legend: {
        position: 'bottom'
      }
    }, false, false)
  }
  else {
    donut.updateOptions({
      plotOptions: {
        pie: {
          offsetY: 20,
        }
      },
      legend: {
        position: 'left'
      }
    }, false, false)
  }
}

$(window).resize(function() {
  mobileDonut()
});
