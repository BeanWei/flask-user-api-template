<template>
<div id="index">
    <Row type="flex" justify="center">
         <Col span="3">
            <h1>{{ msg }}</h1>
            <!-- <Icon type="load-a" size="50" class="loading"></Icon> -->
        </Col> 
        <Button @click="logout">注销</Button>
    </Row>
</div>
</template>

<script>
export default {
    name: 'index',
    data: function() {	
        return {
            msg: ""
        }
    },
    methods: {
        logout() {
            this.$store.commit('del_token')
            this.$router.push('/login')
        }
    },
    created() {
        this.$axios.get("/").then(response => {
            this.msg = response.data
        }).catch(error => {
            console.log(error)
            this.$Message.error(error)
        })
    }
}
</script>

<style lang="less" scoped>
.index {
    background: #f8f8f9;
}
.loading {
    animation: myloading 1s linear infinite;
    margin-top: 100px;
}
@keyframes myloading{
    from {
        transform: rotate(0deg);
    }
    50% {
        transform: rotate(180deg);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>
