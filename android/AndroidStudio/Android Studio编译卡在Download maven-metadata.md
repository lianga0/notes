# AS编译卡在Download maven-metadata

之前在Android Studio里碰到gradle build需要非常长的时间，这是因为gradle每次都同步一下最新的包信息，而网络不好的时候，build的时间就不可控了。

把gradle设置成离线模式就可以改善这个问题，但添加新包后，总要关掉离线模式下载新增的依赖包。

所以还是经常遇见更新代码后第一次编译dowlnad maven-metadata.xml文件卡住半天，最后还是sync fail的问题，最后的解决方法是更换了maven仓库的地址为阿里云。

具体阿里云提供的公共代理仓库请参考[阿里云云效 Maven 是什么](https://developer.aliyun.com/mvn/guide)

<table role="table">
   <colgroup>
      <col style="width: 150px;">
      <col>
      <col>
      <col>
   </colgroup>
   <thead class="next-table-header">
      <tr>
         <th rowspan="1" class="next-table-cell next-table-header-node" role="gridcell">
            <div class="next-table-cell-wrapper"><span style="vertical-align: middle;">仓库名称</span></div>
         </th>
         <th rowspan="1" class="next-table-cell next-table-header-node" role="gridcell">
            <div class="next-table-cell-wrapper"><span style="vertical-align: middle;">阿里云仓库地址</span></div>
         </th>
         <th rowspan="1" class="next-table-cell next-table-header-node" role="gridcell">
            <div class="next-table-cell-wrapper"><span style="vertical-align: middle;">阿里云仓库地址(老版)</span></div>
         </th>
         <th rowspan="1" class="next-table-cell next-table-header-node" role="gridcell">
            <div class="next-table-cell-wrapper"><span style="vertical-align: middle;">源地址</span></div>
         </th>
      </tr>
   </thead>
   <tbody class="next-table-body">
      <tr class="next-table-row first" role="row" table="[object Object]">
         <td class="next-table-cell first" role="gridcell">
            <div class="next-table-cell-wrapper">central</div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/repository/central" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/repository/central</a></div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/nexus/content/repositories/central" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/nexus/content/repositories/central</a></div>
         </td>
         <td class="next-table-cell last" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://repo1.maven.org/maven2/" style="cursor: pointer; color: rgb(27, 154, 238);">https://repo1.maven.org/maven2/</a></div>
         </td>
      </tr>
      <tr class="next-table-row" role="row" table="[object Object]">
         <td class="next-table-cell first" role="gridcell">
            <div class="next-table-cell-wrapper">jcenter</div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/repository/public" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/repository/public</a></div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/nexus/content/repositories/jcenter" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/nexus/content/repositories/jcenter</a></div>
         </td>
         <td class="next-table-cell last" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="http://jcenter.bintray.com/" style="cursor: pointer; color: rgb(27, 154, 238);">http://jcenter.bintray.com/</a></div>
         </td>
      </tr>
      <tr class="next-table-row" role="row" table="[object Object]">
         <td class="next-table-cell first" role="gridcell">
            <div class="next-table-cell-wrapper">public</div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/repository/public" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/repository/public</a></div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/nexus/content/groups/public" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/nexus/content/groups/public</a></div>
         </td>
         <td class="next-table-cell last" role="gridcell">
            <div class="next-table-cell-wrapper">central仓和jcenter仓的聚合仓</div>
         </td>
      </tr>
      <tr class="next-table-row" role="row" table="[object Object]">
         <td class="next-table-cell first" role="gridcell">
            <div class="next-table-cell-wrapper" data-spm-anchor-id="a2c6h.24085988.0.i9.48233054TkE5yD">google</div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper" data-spm-anchor-id="a2c6h.24085988.0.i4.48233054TkE5yD"><a target="_blank" href="https://maven.aliyun.com/repository/google" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/repository/google</a></div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/nexus/content/repositories/google" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/nexus/content/repositories/google</a></div>
         </td>
         <td class="next-table-cell last" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.google.com/" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.google.com/</a></div>
         </td>
      </tr>
      <tr class="next-table-row" role="row" table="[object Object]">
         <td class="next-table-cell first" role="gridcell">
            <div class="next-table-cell-wrapper" data-spm-anchor-id="a2c6h.24085988.0.i10.48233054TkE5yD">gradle-plugin</div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/repository/gradle-plugin" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/repository/gradle-plugin</a></div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/nexus/content/repositories/gradle-plugin" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/nexus/content/repositories/gradle-plugin</a></div>
         </td>
         <td class="next-table-cell last" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://plugins.gradle.org/m2/" style="cursor: pointer; color: rgb(27, 154, 238);">https://plugins.gradle.org/m2/</a></div>
         </td>
      </tr>
      <tr class="next-table-row" role="row" table="[object Object]">
         <td class="next-table-cell first" role="gridcell">
            <div class="next-table-cell-wrapper">spring</div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/repository/spring" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/repository/spring</a></div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/nexus/content/repositories/spring" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/nexus/content/repositories/spring</a></div>
         </td>
         <td class="next-table-cell last" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="http://repo.spring.io/libs-milestone/" style="cursor: pointer; color: rgb(27, 154, 238);">http://repo.spring.io/libs-milestone/</a></div>
         </td>
      </tr>
      <tr class="next-table-row" role="row" table="[object Object]">
         <td class="next-table-cell first" role="gridcell">
            <div class="next-table-cell-wrapper">spring-plugin</div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/repository/spring-plugin" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/repository/spring-plugin</a></div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/nexus/content/repositories/spring-plugin" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/nexus/content/repositories/spring-plugin</a></div>
         </td>
         <td class="next-table-cell last" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="http://repo.spring.io/plugins-release/" style="cursor: pointer; color: rgb(27, 154, 238);">http://repo.spring.io/plugins-release/</a></div>
         </td>
      </tr>
      <tr class="next-table-row" role="row" table="[object Object]">
         <td class="next-table-cell first" role="gridcell">
            <div class="next-table-cell-wrapper">grails-core</div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/repository/grails-core" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/repository/grails-core</a></div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/nexus/content/repositories/grails-core" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/nexus/content/repositories/grails-core</a></div>
         </td>
         <td class="next-table-cell last" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://repo.grails.org/grails/core" style="cursor: pointer; color: rgb(27, 154, 238);">https://repo.grails.org/grails/core</a></div>
         </td>
      </tr>
      <tr class="next-table-row last" role="row" table="[object Object]">
         <td class="next-table-cell first" role="gridcell">
            <div class="next-table-cell-wrapper">apache snapshots</div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/repository/apache-snapshots" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/repository/apache-snapshots</a></div>
         </td>
         <td class="next-table-cell" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://maven.aliyun.com/nexus/content/repositories/apache-snapshots" style="cursor: pointer; color: rgb(27, 154, 238);">https://maven.aliyun.com/nexus/content/repositories/apache-snapshots</a></div>
         </td>
         <td class="next-table-cell last" role="gridcell">
            <div class="next-table-cell-wrapper"><a target="_blank" href="https://repository.apache.org/snapshots/" style="cursor: pointer; color: rgb(27, 154, 238);">https://repository.apache.org/snapshots/</a></div>
         </td>
      </tr>
   </tbody>
</table>

修改build.gradle文件中repositories，如下：

```
buildscript {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/public'}
        maven { url 'https://maven.aliyun.com/repository/gradle-plugin' }
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'http://maven.aliyun.com/nexus/content/groups/public/' }
    }
    dependencies { // ....
    }
}
 
allprojects {
    repositories {
        maven { url "https://maven.google.com" } //这一行必须去掉
        maven { url 'https://maven.aliyun.com/repository/public'}
        maven { url 'https://maven.aliyun.com/repository/gradle-plugin' }
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'http://maven.aliyun.com/nexus/content/groups/public/' }
        maven { url "https://jitpack.io" }
    }
}
```

## gradle 国内为什么慢

由于默认情况下执行 gradle 各种命令是去国外的 gradle 官方镜像源获取需要安装的具体软件信息，所以在不使用代理、不翻墙的情况下，从国内访问国外服务器的速度相对比较慢

## 如何修改镜像源

阿里旗下维护着一个国内 maven 镜像源，同样适用于 gradle。到目前为止npm、yarn、maven、composer 的国内加速方案都可以使用着阿里旗下提供的国内镜像源

### a). 配置只在当前项目生效

在 `build.gradle` 文件内修改/添加 `repositories` 配置

```
repositories {
    maven {
        url "http://maven.aliyun.com/nexus/content/groups/public"
    }
}
```

### b). 配置全局生效

找到 `(用户家目录)/.gradle/init.gradle` 文件，如果找不到 `init.gradle` 文件，自己新建一个

修改/添加 `init.gradle` 文件内的 `repositories` 配置

```
allprojects {
    repositories {
        maven {
            url "http://maven.aliyun.com/nexus/content/groups/public"
        }
    }
}
```

### 验证是否修改成功

在 build.gradle 文件内增加一个任务

```
task showRepos {
    doLast {
        repositories.each {
            println "repository: ${it.name} ('${it.url}')"
        }
    }
}
```

然后执行 gradle -q showRepos 任务，如果输出了刚刚配置的地址就说明修改成功，如下：

```
$ gradle -q showRepos
repository: maven ('http://maven.aliyun.com/nexus/content/groups/public')
```

Reference：[gradle 国内加速，修改镜像源](https://ld246.com/article/1536205523784)
