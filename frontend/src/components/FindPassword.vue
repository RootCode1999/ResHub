//找回密码

<template>

<div>
<!--   -->
  <div class="findPa" id="findPa" @keyup.enter="verify_verificationCode">
    <div class="log-bg">
        <div class="log-cloud cloud1"></div>
        <div class="log-cloud cloud2"></div>
        <div class="log-cloud cloud3"></div>
        <div class="log-cloud cloud4"></div>

        <div class="findPa-logo" @click="backToHome">Waiting for you!</div>
        <div class="findPa-text">@reshub team</div>
    </div>
    <div class="findPa-email">
        <input type="text" placeholder="Email" class="findPa-input" v-model="mail">
        <input type="password" placeholder="new password" class='findPa-input' v-model="password">
        <input type="password" placeholder="new password again" class='findPa-input' v-model="password2">

        <!-- 验证码  -->
        <input type="text" placeholder="verification code" class='findPa-input2'  v-model="verificationCode">
      <el-button style="width: 110px;height: 50px;" class="primary" @click="askVerificationCode" :disabled="disabled">
        {{timeContent}}
      </el-button>

        <div class="errorMessage">{{errorMessage}}</div>
        <span class="findPa-btn" @click="verify_verificationCode">重置密码</span>
        <span class="findPa-btn" @click="backToLogin">返回登录</span>
        <span class="findPa-btn" @click="verify_verificationCode">测试验证码验证</span>

        <!-- for debug
        <input type="text" placeholder="testVar" class="findPa-input" v-model="testVar">
        <span class="findPa-btn" @click="test">测试</span>-->
    </div>
  </div>
</div>
</template>

<script>
    import crypto from 'crypto'
    import TopBar from "./TopBar";
    import Loading from './Loading.vue'
    import axios from 'axios'
    import baseUrl from './baseUrl'
    export default {
        name: "FindPassword",
        data(){
            return {
                mail:'',
                verificationCode:'',
                veri_success: false,
                password: '',
                password2: '',
                errorMessage:'',//出错提示信息
                timeLeft: true,
                testVar:'',
              disabled:false,
              timeContent: '发送验证码',
            }
        },
        methods:{
            


          //发送验证码
          askVerificationCode() {
            let _this = this;
            //计时器
            if(this.timeContent=='发送验证码'){
              let time=59;
              let timer=setInterval(()=>{
                if(time>0){
                  this.timeContent=time+'s';
                  this.disabled=true;
                  time--;
                }
                else{
                  window.clearInterval(timer);
                  this.disabled=false;
                  this.timeContent='发送验证码';
                }
              },1000);
            }
            console.log('这个就是Email:'+_this.mail);
            axios.get(baseUrl+'/passwordLost',{
              params:{
                mailAddress:_this.mail
              }
            })

              .then(function (response){
                //Toast(response.data.message);
                console.log(response);
                //_this.subidcode = response.data.result;
                console.log('askVerificationCode:response.data.result:'+response.data.result);
              })
              .catch(function (error) { // 请求失败处理
                console.log(error);
              });
          },
          //let data = new FormData();
            //data.append('userId',this.useremail);
            //axios.get(baseUrl+'/passwordLost',data)


            //验证码验证
            verify_verificationCode(){
                let _this=this;
                _this.veri_success=false;
                //要求验证码必须为6位数字
                let verificationCode_pattern=/^[0-9]{6}$/;
                if(verificationCode_pattern.test(_this.verificationCode)==false){
                    console.log('verificationCode_pattern error');
                    this.errorMessage='验证码为6位数字';
                    return false;
                }
                axios.get(baseUrl+'/verificationCode',{
                    params:{
                        mailAddress: _this.mail,
                        verificationCode:_this.verificationCode
                    }
                    
                })
                .then(function(response){
                    console.log('验证码验证返回的response.data.result:'+response.data.result);
                    _this.veri_success=response.data.result;
                    
                    if(_this.veri_success==false){
                        _this.errorMessage='验证码错误';  
                    }
                    console.log('验证码验证最后,_this.veri_success:'+_this.veri_success);
                    
                    _this.ResetPassword();
                    
                })
                
            },
            //邮件和密码的格式验证
            patternMatching2(mail,pa,pa2){
                this.errorMessage='';
                //Email地址
                let mail_pattern=/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
                //密码(以字母开头，长度在6~18之间，只能包含字母、数字和下划线)
                let password_pattern=/^\w{6,18}$/;
                if(mail_pattern.test(mail)==false){
                    console.log('mail_pattern error');
                    this.errorMessage='邮件格式错误';
                    return false;
                }
                //验证两次输入的密码是否一致
                if(pa!=pa2){
                    console.log('two password not same');
                    this.errorMessage='两次输入的密码不一致';
                    return false;
                }
                else if(password_pattern.test(pa)==false){
                        console.log('password_pattern error');
                        //分情况提示错误信息
                        //console.log('password is '+pa);
                        //console.log('password-length is:'+pa.length);

                        if(pa.length<6||pa.length==0){

                            this.errorMessage='密码长度必须大于6';
                        }
                        else if(pa.length>18){
                            this.errorMessage='密码长度必须小于18';
                        }
                        else {
                            this.errorMessage='只能含有字母、数字、下划线';
                        }

                        return false;
                }
                else {
                    return true;
                }

            },
            //要求重置密码
            ResetPassword(){
                let _this=this;
                _this.errorMessage='重置密码';
                let successTmp;
                //验证邮件地址和密码的格式
                successTmp=_this.patternMatching2(_this.mail,_this.password,_this.password2);
                console.log('pattern is right? '+successTmp);
                if(successTmp!=true){
                    return;
                }
                
                //验证验证码正确
                //_this.verify_verificationCode();
                console.log('重置密码中验证验证码正确返回的结果： '+_this.veri_success);
                if(_this.veri_success!=true){
                    return;
                }
                

                //md5加密
                const md5 = crypto.createHash('md5');
                md5.update(_this.password);
                let md5password = md5.digest('hex') ;

                //重置密码的接口
                axios.get(baseUrl+'/newPassword',{
                    params:{
                        mailAddress: _this.mail,
                        newPassword: md5password
                        }
                })
                .then(function(response){
                       console.log('进入重置');
                       console.log('重置response.data.result：'+response.data.result);
                       var reset_success;
                       reset_success=response.data.result;
                       if(reset_success==true){
                           console.log('重置成功');
                           _this.$router.push({
                            path:'/login',
                            });
                       }
                       else {
                           console.log('重置失败');
                           _this.errorMessage='重置失败'
                       }
                })
                

            },
            backToLogin(){
                this.$router.push({
                    path:'/login',
                });
            },
            backToHome(){
                this.$router.push({
                    path:'/',
                });
            }
        }
    }
</script>

<style scoped>
.errorMessage{
    text-align: center; margin-top: 20px;margin-bottom: 20px;color: #f88787;
}
.findPa{position: absolute; overflow: hidden;left: 50%; margin-left: -250px;top:3%; width: 500px; min-height: 555px;margin-bottom: 3%;
padding-bottom: 30px;
z-index: 10; background: #fff;-webkit-border-radius: 5px;
-moz-border-radius: 5px;
-ms-border-radius: 5px;
-o-border-radius: 5px;
border-radius: 5px; -webkit-box-shadow:  0px 3px 16px -5px #070707; box-shadow:  0px 3px 16px -5px #070707}

.log-cloud{background-image: url(../assets/login-cloud.png); width: 63px ;height: 40px; position: absolute; z-index: 1}
.findPa .cloud1{top:21px; left: -30px; transform: scale(.6); animation: cloud1 20s linear infinite;}
.findPa .cloud2{top:87px; right: 20px; animation: cloud2 19s linear infinite;}
.findPa .cloud3{top:160px; left: 5px;transform: scale(.8);animation: cloud3 21s linear infinite;}
.findPa .cloud4{top:150px; left: -40px;transform: scale(.4);animation: cloud4 19s linear infinite;}
.log-bg{background: url(../assets/login-bg.jpg); width: 100%; height: 312px; overflow: hidden;}
.findPa-logo{height: 80px; margin: 120px auto 25px; text-align: center; color: #1fcab3; font-weight: bold; font-size: 40px; cursor: pointer;}
.findPa-text{color: #57d4c3; font-size: 13px; text-align: center; margin: 0 auto;}
.findPa-logo,.findPa-text{z-index: 2}


/*1*/
.findPa-btns{padding: 15px 0; margin: 0 auto;}
.findPa-btn{width:402px; display: block; text-align: left; line-height: 50px;margin:0 auto 15px; height:50px; color:#fff;
font-size:13px;-webkit-border-radius: 5px; background-color: #3B5999;
-moz-border-radius: 5px;
-ms-border-radius: 5px;
-o-border-radius: 5px;
border-radius: 5px;
position: relative;
cursor: pointer;
}
.findPa-btn.tw{background-color: #13B4E9}
.findPa-btn.email{background-color: #50E3CE}
.findPa-btn:hover,.findPa-btn:focus{color: #fff; opacity: .8;}
.findPa-email .findPa-btn{background-color: #50E3CE;text-align: center;}
.findPa-email{text-align: center; margin-top: 20px;}

/*.findPa-input-empty{border: 1px solid #f37474 !important;}*/
.isloading{background: #d6d6d6}

.findPa-input{width: 370px;overflow: hidden; padding: 0 15px;font-size: 13px; border: 1px solid #EBEBEB; margin:0 auto 15px; height: 48px; line-height: 48px; -webkit-border-radius: 5px;
-moz-border-radius: 5px;
-ms-border-radius: 5px;
-o-border-radius: 5px;
border-radius: 5px;}
.findPa-input.warn{border: 1px solid #f88787}
/*2 begin*/
/*.findPa-btn2s{padding: 15px 0; margin: 0 auto;}
.findPa-btn2{text-align: left; line-height: 50px;margin:0 auto 15px; height:50px; color:#fff;
font-size:13px;-webkit-border-radius: 5px; background-color: #3B5999;
-moz-border-radius: 5px;
-ms-border-radius: 5px;
-o-border-radius: 5px;
border-radius: 5px;
position: relative;}
.findPa-btn2.tw{background-color: #13B4E9}
.findPa-btn2.email{background-color: #50E3CE}
.findPa-btn2:hover,.findPa-btn2:focus{color: #fff; opacity: .8;}
.findPa-email .findPa-btn2{background-color: #50E3CE;text-align:center}
.findPa-btn2 .text{left: 95px; line-height: 50px; text-align: left; position: absolute;}*/

.sendVeri{
    text-align: center;
    color:  #50E3CE;
    cursor: pointer;
    width: 30px;

}
.sendVeri:hover{
    color: #b8f0e4;
}

.findPa-input2{width: 255px;overflow: hidden; padding: 0 15px;font-size: 13px; border: 1px solid #EBEBEB; margin:0 auto 15px; height: 48px; line-height: 48px; -webkit-border-radius: 5px;
-moz-border-radius: 5px;
-ms-border-radius: 5px;
-o-border-radius: 5px;
border-radius: 5px;}
.findPa-input2.warn{border: 1px solid #f88787}


/*2 end*/
 @-webkit-keyframes cloud1 {
    0%{left: 200px}
    100%{left:-130px;}
}
@keyframes cloud1{
    0%{left: 200px}
    100%{left:-130px;}
}

 @-webkit-keyframes cloud2 {
    0%{left:500px;}
    100%{left:-90px;}
}
@keyframes cloud2{
    0%{left:500px;}
    100%{left:-90px;}
}

@-webkit-keyframes cloud3 {
    0%{left:620px;}
    100%{left:-70px;}
}
@keyframes cloud3{
    0%{left:620px;}
    100%{left:-70px;}
}@-webkit-keyframes cloud4 {
    0%{left:100px;}
    100%{left:-70px;}
}
@keyframes cloud4{
    0%{left:100px;}
    100%{left:-70px;}
}

</style>

