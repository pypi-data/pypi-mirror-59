apputiljs = function () {
    class Switch {
        constructor(turnOn, turnOff) {
            this.status = 'off';
            this.turnOn = (e) => {
                turnOn(e);
                this.status = 'on';
            };
            this.turnOff = (e) => {
                turnOff(e);
                this.status = 'off';
            };
        }

        reverse(e) {
            if (this.status === 'on') this.turnOff(e);
            else this.turnOn(e);
            return this;
        }

        bindKey(dic) {

            if (dic.on) {
                jwerty.key(dic.on, (e) => {
                    this.turnOn(e)
                });
            }
            if (dic.off) {
                jwerty.key(dic.off, (e) => {
                    this.turnOff(e)
                })
            }
            if (dic.reverse) {
                console.log("dic:", dic.reverse);
                jwerty.key(dic.reverse, (e) => {
                    console.log('reverse');
                    this.reverse(e)
                })
            }
            return this;
        }
    }

    var simpleMaximaze=function (el) {
        el.appendTo($("body"));
        $("body").height("100%");
        $("body").width("100%");
        el[0].style = el[0].style + `
            position:fixed;
            left:0;top:0;right:0;bottom:0;
            z-index:65535;
            padding:30px;
            box-sizing:bordered-box;
            overflow:auto;
        `;
        el.css("min_height","100%");
        el.css("width","100%");
        el.css('position','fixed')
    };

    return {
        simpleMaximaze,
        Switch
    }
}();