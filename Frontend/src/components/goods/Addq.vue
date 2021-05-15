<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>问题管理</el-breadcrumb-item>
      <el-breadcrumb-item>添加问题</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图 -->
    <el-card>
      <!-- 提示 -->
      <el-alert title="添加问题信息" type="info" center show-icon :closable="false"></el-alert>
      <!-- 步骤条 -->
      <el-steps :space="400" :active="activeIndex - 0" finish-status="success" align-center>
        <el-step title="基本信息"></el-step>
        <el-step title="设置赏金"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>

      <!-- Tab栏 -->
      <el-form
        :model="addForm"
        :rules="addFormRules"
        ref="addFormRef"
        label-width="100px"
        label-position="top"
      >
        <el-tabs
          v-model="activeIndex"
          :tab-position="'left'"
          :before-leave="beforeTabLeave"
        >
          <el-tab-pane label="基本信息" name="0">
            <el-form-item label="问题主题" prop="theme">
              <el-input v-model="addForm.theme"></el-input>
            </el-form-item>
            <el-form-item label="问题详情" prop="detail">
              <el-input v-model="addForm.detail" type = "textarea" rows="5"></el-input>
            </el-form-item>
            <el-form-item label="问题分类" prop="question_cat">
              <el-select v-model="addForm.tag" placeholder="请选择" @change="handleChange()">
                <el-option
                  v-for="item in cateList"
                  :key="item.id"
                  :label="item.tag"
                  :value="item.tag">
                </el-option>
              </el-select>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="设置赏金" name="1">
            <el-form-item label="赏金金额" prop="t">
              <el-input v-model="addForm.reward" type = "number"></el-input>
            </el-form-item>
            <el-button type="primary" class="btnAdd" @click="addQuestion">完成</el-button>
          </el-tab-pane>
        </el-tabs>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // 步骤条默认激活 与左侧Tab联动
      activeIndex: '0',
      // 添加商品的表单对象
      addForm: {
        username: window.sessionStorage.getItem('token'),
        theme: '',
        detail: '',
        reward: 0,
        tag: ''
      },
      addFormRules: {
        theme: [
          { required: true, message: '请输入问题主题', trigger: 'blur' }
        ],
        detail: [
          { required: true, message: '请输入问题详情', trigger: 'blur' }
        ],
        reward: [
          { required: true, message: '请输入悬赏金额', trigger: 'blur' }
        ],
        tag: [
          { required: true, message: '请选择问题分类', trigger: 'blur' }
        ]
      },
      // 商品列表
      cateList: [{ tag: '校园', id: '1' },
        { tag: '学习', id: '2' },
        { tag: '恋爱', id: '3' },
        { tag: '娱乐', id: '4' },
        { tag: '生活', id: '5' }]
    }
  },
  created () {
  },
  computed: {
  },
  methods: {
    // tag选择器选中项变化时出发
    handleChange () {
      console.log(this.addForm.tag)
    },
    beforeTabLeave () {
      return true
    },
    // 添加问题
    addQuestion () {
      this.$refs.addFormRef.validate(async valid => {
        if (!valid) return this.$message.error('请填写必要的表单项！')
        // 发送请求前：需对提交的表单进行处理goods_cat attrs
        const { data: res } = await this.$http.get('http://127.0.0.1:5000/addq', {
          params: this.addForm
        })
        if (res.meta.status === 300) {
          return this.$message.error('您当前账户余额不足！')
        } else {
          this.$router.push('/myquestion')
          return this.$message.success('添加问题成功！')
        }
      })
    }
  }
}
</script>

<style lang='less' scoped>
.el-checkbox {
  margin: 0 8px 0 0 !important;
}
.previewImg{
  width: 100%;
}
.btnAdd{
  margin-top: 15px
}
</style>
