<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>委托浏览</el-breadcrumb-item>
      <el-breadcrumb-item>问题委托</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图 -->
    <el-card>

      <!-- 订单列表 -->
      <el-table :data="orderList" border stripe>
        <el-table-column type="index" label="#"></el-table-column>
        <el-table-column label="问题主题" prop="theme"></el-table-column>
        <el-table-column label="悬赏金额" prop="reward"></el-table-column>
        <el-table-column label="是否已结束">
          <template slot-scope="scope">
            <el-tag type="danger" size="mini" v-if="scope.row.isfinished">已有满意回答</el-tag>
            <el-tag type="success" size="mini" v-else>未结束</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="创建时间" prop="create_time"></el-table-column>
        <el-table-column label="tag" prop="tag" width = "80px"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" icon="el-icon-edit" @click="showEditDialog(scope.row.id)" :disabled="scope.row.isfinished">提交回答</el-button>
            <el-button
              type="success"
              size="mini"
              icon="el-icon-location"
              @click="showProgressDialog(scope.row.detail)"
            >详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页区域 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.pagenum"
        :page-sizes="[5, 10, 15, 20]"
        :page-size="queryInfo.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
    </el-card>

    <!-- 编辑对话框 -->
    <el-dialog
      title="提交回答"
      :visible.sync="addressDialogVisible"
      width="50%"
    >
      <el-form
        :model="answer"
        :rules="addressFormRules"
        ref="addressFormRef"
        label-width="100px"
      >
        <el-form-item label="您的答案" prop="address2">
          <el-input
            type="textarea"
            :autosize="{ minRows: 4}"
            placeholder="请输入回答"
            maxlength="817"
            show-word-limit
            v-model="answer.detail"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
          <el-button @click="addressDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="answerQuestionByid()">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="委托详细内容" :visible.sync="progressDialogVisible" width="50%">{{detail}}</el-dialog>
  </div>
</template>

<script>

export default {
  data () {
    return {
      // 订单列表查询参数
      queryInfo: {
        query: '',
        pagenum: 1,
        pagesize: 10
      },
      total: 0,
      // 订单列表
      orderList: [],
      // 接受任务的参数
      takeInfo: {
        taskId: 0,
        receiver: window.sessionStorage.getItem('token')
      },
      // 修改地址对话框
      addressDialogVisible: false,

      addressFormRules: {
        address2: [
          { required: true, message: '确认答案是否合规', trigger: 'blur' }
        ]
      },
      answer: {
        detail: '',
        q_id: 0,
        username: window.sessionStorage.getItem('token')
      },
      // 物流进度对话框
      progressDialogVisible: false,
      // 物流进度
      detail: ''
    }
  },
  created () {
    this.getQuestionList()
  },
  methods: {
    async getQuestionList () {
      console.log(this.queryInfo)
      const { data: res } = await this.$http.get('http://127.0.0.1:5000/questionList', {
        params: this.queryInfo
      })
      if (res.meta.status !== 200) {
        return this.$message.error('获取订单列表失败！')
      }
      console.log(res)
      this.total = res.data.total
      this.orderList = res.data.questionList
    },
    // 分页
    handleSizeChange (newSize) {
      this.queryInfo.pagesize = newSize
      this.getQuestionList()
    },
    handleCurrentChange (newSize) {
      this.queryInfo.pagenum = newSize
      this.getQuestionList()
    },
    showEditDialog (id) {
      this.addressDialogVisible = true
      this.answer.q_id = id
    },
    async answerQuestionByid () {
      const confirmResult = await this.$confirm(
        '回答提交后不可更改, 是否继续?',
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
      const { data: res } = await this.$http.get('http://127.0.0.1:5000/addAnswer', {
        params: this.answer
      })
      if (res.meta.status === 101) return this.$message.error('有敏感词汇，提交回答失败！')
      this.$message.success('提交回答成功！')
      this.$refs.addressFormRef.resetFields()
      this.addressDialogVisible = false
      this.getQuestionList()
    },
    async showProgressDialog (detail) {
      // 供测试的物流单号：1106975712662
      this.detail = detail
      this.progressDialogVisible = true
    }
  }
}
</script>

<style lang="less" scoped>
.el-cascader {
  width: 100%;
}
</style>
