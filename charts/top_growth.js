var app = Vue.createApp({
    data() {
        return {
            sbiChartHash:null,
            stocks:top_growth,
            updatetime:new Date(Date.parse(top_growth_updatetime)),
            updateCommand:top_growth_update_command,
            checkedFlags:[],
            FlagFilterMode:"OR",
            InvestamtFrom:NaN,
            InvestamtTo:NaN,
            Count:null,
            Markets:[...new Set(top_growth.map(item => item.market))]
        };
    },
    mounted() {
      this.sbiChartHash = hash_code||localStorage.sbiChartHash||null;
      this.checkedFlags = JSON.parse(localStorage.getItem('checkedFlags')) || [];
      this.FlagFilterMode= localStorage.FlagFilterMode||"OR";
      this.InvestamtFrom= localStorage.InvestamtFrom||NaN;
      this.InvestamtTo= localStorage.InvestamtTo||NaN;
    },
    watch: {
      sbiChartHash(newVal) {
        localStorage.sbiChartHash = newVal;
      },
      FlagFilterMode(newVal) {
        localStorage.FlagFilterMode = newVal;
      },
      InvestamtFrom(newVal){
        localStorage.InvestamtFrom = newVal;
      },
      InvestamtTo(newVal){
        localStorage.InvestamtTo = newVal;
      },
      checkedFlags:{
          handler(val, oldVal){
            localStorage.setItem('checkedFlags', JSON.stringify(this.checkedFlags));
          },
          deep:true
      }
    },
    methods: {
      SBILink: function (code) {
        return "https://site1.sbisec.co.jp/ETGate/?_ControlID=WPLETsiR001Control&stock_sec_code_mul=" + code
                + "&_ActionID=getDetailOfStockPriceJP&_PageID=WPLETsiR001Ilst10";
      },
      ChartImg: function (code) {
        return "img/" + code+".svg";
      },
      SBI5MinChart:function(code,hash){
        return "https://chart.iris.sbisec.co.jp/sbi/gchart/gc1/CHART.cgi?hash=" + hash +"&type=real&ricCode=" + code + ".T&mode=5&size=1&main=B3&sub=V&PreP=1&template=CHART01M.ini"
      },

      SBI6MonthChart:function(code,hash){
        return "https://chart.iris.sbisec.co.jp/sbi/as/Mchart-mchart.html?ricCode=" + code + ".T&type=real&hash=" + hash +"&size=0&mode=D&DispNum=120&main=C&addon=SMA3&sub=V&TP=1&side=0&exdvMark=0&param1=5&param2=20&param3=100&diffquote=None&rand=1629437618120"
        // return "https://chart.iris.sbisec.co.jp/sbi/gchart/gc1/CHART.cgi?hash=" + hash +"&type=real&ricCode=" + code + ".T&mode=5&size=1&main=B3&sub=V&PreP=1&template=CHART01M.ini"
      },

      FilterdStocks(){
        list=this.stocks.filter((st)=>{
            // フラグでフィルター
            return this.checkedFlags.some((f)=>st.market==f);
        });
        return list.sort((a,b)=>parseFloat(b.growth_per)-parseFloat(a.growth_per));

        // list=this.stocks.filter((st)=>{
          //     // フラグでフィルター
          //     if(this.FlagFilterMode=="AND") {
          //       return this.checkedFlags.every((f)=>st.flags[f]);
          //     }
          //     if(this.FlagFilterMode=="OR") {
          //       return this.checkedFlags.some((f)=>st.flags[f]);
          //     }
          // });
          // //金額フィルター
          // if(this.InvestamtFrom){
          //   list=list.filter((st)=>{
          //     return this.TradingPrice(st.stock)>=(this.InvestamtFrom*10000);
          //   })
          // }
          // if(this.InvestamtTo){
          //   list=list.filter((st)=>{
          //     return this.TradingPrice(st.stock)<=(this.InvestamtTo*10000);
          //   })
          // }
          // this.Count= list.length
          // return list;
      },
      ActiveFlags(stock){
        return Object.keys(stock.flags).filter((k)=>stock.flags[k]);
      },
      TradingPrice(stock){
        return parseFloat(stock.close_price)*parseFloat(stock.trading_unit);
      }
    }
});

app.mount("#app");