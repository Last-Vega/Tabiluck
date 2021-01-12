<!-- nakano -->
<template>
    <div>
        <label v-if="!value.image" class="upload-content-space user-photo default">
            <input ref="file" class="file-button" type="file" @change="upload" />
            画像をアップロード
        </label>

        <div v-if="value.image" class="uploaded">
            <label class="upload-content-space user-photo">
                <input ref="file" class="file-button" type="file" @change="upload" />
                <img class="user-photo-image" :src="value.image" />
                {{ value.imageName }}
            </label>
            <button type="button" class="delete-button" @click="deleteImage">
                削除する
            </button>
        </div>

        <ul v-if="fileErrorMessages.length > 0" class="error-messages">
            <li v-for="(message, index) in fileErrorMessages" :key="index">
                {{ message }}
            </li>
        </ul>
    </div>
</template>

<script>
/* eslint-disable */
export default {
    name: 'Upload',
    props: {
        value: {
            type: Object,
            default: null
        },

    },
    data() {
        return {
            file: null,
            fileErrorMessages: []
        }
    },
    methods: {
        async upload(event) {
            const files = event.target.files || event.dataTransfer.files
            const file = files[0]
            if (this.checkFile(file)) {
                const picture = await this.getBase64(file)
                this.$emit('input', {image: picture, imageName: file.name})
            }
        },
        deleteImage() {
            this.$emit('input', {image: null, imageName: null})
            this.$refs.file = null
        },
        getBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader()
                reader.readAsDataURL(file)
                reader.onload = () => resolve(reader.result)
                reader.onerror = error => reject(error)
            })
        },
        checkFile(file) {
            let result = true
            this.fileErrorMessages = []
            const SIZE_LIMIT = 5000000 // 5MB
            // キャンセルしたら処理中断
            if (!file) {
                result = false
            }
            // jpeg か png 関連ファイル以外は受付けない
            if (file.type !== 'image/jpeg' && file.type !== 'image/png') {
                this.fileErrorMessages.push('アップロードできるのは jpeg画像ファイル か png画像ファイルのみです。')
                result = false
            }
            // 上限サイズより大きければ受付けない
            if (file.size > SIZE_LIMIT) {
                this.fileErrorMessages.push('アップロードできるファイルサイズは5MBまでです。')
                result = false
            }
            return result
        }
    }
 }
</script>

<style scoped>
.user-photo {
  cursor: pointer;
  outline: none;
}

.user-photo.default {
  align-items: center;
  background-color: #368c97;
  border: 1px solid #296b74;
  border-radius: 2px;
  box-sizing: border-box;
  display: inline-flex;
  font-weight: 600;
  justify-content: center;
  letter-spacing: 0.3px;
  color: #fff;
  height: 30px;
  padding: 10px;
  margin: 5px 0px;
  max-width: 177px;
}

.user-photo.default:hover {
  background-color: #368c97;
}

.user-photo.default:active {
  background-color: #296b74;
}

.user-photo-image {
  max-width: 85px;
  display: block;
}

.user-photo-image:hover {
  opacity: 0.8;
}

.file-button {
  display: none;
}

.uploaded {
  align-items: center;
  display: flex;
}

.delete-button {
    background-color: #fff;
    border: none;
    color: #368c97;
    margin-left: 2rem;
    padding: 0;
    }

.delete-button:hover {
    text-decoration: underline;
}

.error-messages {
    color: #cf0000;
    list-style: none;
}
</style>
