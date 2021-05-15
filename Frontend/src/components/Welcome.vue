<template>
  <div>
    <el-row style="margin-top:10px;">
      <el-col :span="24">
        <div class="grid-content bg-purple-dark">
          <el-card >
            <div slot="header" >
              <span>个人中心</span>
            </div>
            <div class="name-role">
              <span class="sender">{{ userData.username }} - {{ userData.nickname }}</span>
            </div>
            <el-row>
              <el-col :span="24">
                <div class="grid-content bg-purple">
                  <div class="personal-relation">
                    <div class="relation-item">积分:
                      <div style="float: right; padding-right:20px;">{{userData.score}}
                      </div>
                    </div>
                  </div>
                </div>
              </el-col>
              <el-col :span="24">
                <div class="grid-content bg-purple-light">
                  <div class="personal-relation">
                    <div class="relation-item">余额:
                      <div style="float: right; padding-right:20px;">{{userData.balance}}
                      </div>
                    </div>
                  </div>
                </div>
              </el-col>
              <el-col :span="24">
                <div class="grid-content bg-purple">
                  <div class="personal-relation">
                    <div class="relation-item">手机号:
                      <div style="float: right; padding-right:20px;">{{userData.phone}}
                      </div>
                    </div>
                  </div>
                </div>
              </el-col>
              <el-col :span="24">
                <div class="grid-content bg-purple-light">
                  <div class="personal-relation">
                    <div class="relation-item">邮箱:
                      <div style="float: right; padding-right:20px;">{{userData.email}}
                      </div>
                    </div>
                  </div>
                </div>
              </el-col>
              <el-col :span="24"><div class="grid-content row-bg"></div></el-col>
              <el-button type="primary"
                         size="median"
                         icon="el-icon-edit"
                         @click="editDialogVisible=true">修改个人信息</el-button>

            </el-row>
          </el-card>
        </div>
      </el-col>

    </el-row>
    <!-- 修改用户的对话框 -->
    <el-dialog
      title="修改用户信息"
      :visible.sync="editDialogVisible"
      width="50%"
      @close="editDialogClosed"
    >
      <!-- 内容主体 -->
      <el-form
        :model="editUserForm"
        ref="editUserFormRef"
        :rules="editUserFormRules"
        label-width="70px"
      >
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="editUserForm.nickname"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editUserForm.email"></el-input>
        </el-form-item>
        <el-form-item label="手机" prop="phone">
          <el-input v-model="editUserForm.phone"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editUser">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data () {
    var checkEmail = (rule, value, callback) => {
      const regEmail = /^\w+@\w+(\.\w+)+$/
      if (regEmail.test(value)) {
        // 合法邮箱
        return callback()
      }
      callback(new Error('请输入合法邮箱'))
    }
    // 自定义手机号规则
    var checkphone = (rule, value, callback) => {
      const regphone = /^1[34578]\d{9}$/
      if (regphone.test(value)) {
        return callback()
      }
      // 返回一个错误提示
      callback(new Error('请输入合法的手机号码'))
    }
    return {
      userData: {
        username: 'admin',
        score: 0,
        nickname: '',
        balance: 0,
        email: '',
        phone: ''
      },
      editDialogVisible: false,
      editUserForm: {},
      // 编辑用户表单验证
      editUserFormRules: {
        nickname: [
          { required: true, message: '请输入昵称', trigger: 'blur' },
          {
            min: 2,
            max: 10,
            message: '昵称的长度在2～10个字',
            trigger: 'blur'
          }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { validator: checkEmail, trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { validator: checkphone, trigger: 'blur' }
        ]
      }
    }
  },
  created () {
    this.getUserData()
  },
  methods: {
    async getUserData () {
      const { data: res } = await this.$http.get('http://127.0.0.1:5000/getUserInfo', {
        params: { 'username': window.sessionStorage.getItem('token') }
      })
      if (res.meta.status !== 200) {
        return this.$message.error('获取用户数据失败！')
      }
      this.userData = res.data
    },
    resetForm () {
    },
    editDialogClosed () {
      this.resetForm()
    },
    async editUser () {
      // 提交请求前，表单预验证
      this.$refs.editUserFormRef.validate(async valid => {
        // console.log(valid)
        // 表单预校验失败
        if (!valid) return
        const confirmResult = await this.$confirm(
          '确认修改?',
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).catch(err => err)
        // 点击确定 返回值为：confirm
        // 点击取消 返回值为： cancel
        if (confirmResult !== 'confirm') {
          return this.$message.info('已取消')
        }
        const { data: res } = await this.$http.get('http://127.0.0.1:5000/editUser', {
          params: {
            data: this.editUserForm,
            username: this.userData.username
          }
        })
        if (res.meta.status !== 200) return this.$message.error('修改失败！')
        this.$message.success('修改成功！')
        this.editDialogVisible = false
        this.getUserData()
      })
    }
  }

}
</script>

<style lang="less" scoped>
.relation-item {
  padding: 12px;
}
.name-role {
  font-size: 16px;
  padding: 5px;
  text-align:center;
}
.dialog-footer{
  padding-top:10px ;
  padding-left: 10%;
}
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
</style>
