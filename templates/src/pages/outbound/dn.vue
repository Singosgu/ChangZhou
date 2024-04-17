<template>
  <div>
    <transition appear enter-active-class="animated fadeIn">
      <q-table
        class="my-sticky-header-column-table shadow-24"
        :data="table_list"
        row-key="id"
        :separator="separator"
        :loading="loading"
        :filter="filter"
        :columns="columns"
        hide-bottom
        :pagination.sync="pagination"
        no-data-label="No data"
        no-results-label="No data you want"
        :table-style="{ height: height }"
        flat
        bordered
        selection="multiple"
        :selected.sync="selected"
      >
        <template v-slot:top>
          <q-btn-group push>
<!--            <q-btn-->
<!--              v-show="-->
<!--                $q.localStorage.getItem('staff_type') !== 'Supplier' &&-->
<!--                $q.localStorage.getItem('staff_type') !== 'Customer' &&-->
<!--                $q.localStorage.getItem('staff_type') !== 'Inbound' &&-->
<!--                $q.localStorage.getItem('staff_type') !== 'StockControl' &&-->
<!--                $q.localStorage.getItem('is_vip') === 9-->
<!--              "-->
<!--              :label="$t('new')"-->
<!--              icon="add"-->
<!--              @click="newFormOpen()"-->
<!--            >-->
<!--              <q-tooltip-->
<!--                content-class="bg-amber text-black shadow-4"-->
<!--                :offset="[10, 10]"-->
<!--                content-style="font-size: 12px"-->
<!--              >{{ $t("newtip") }}-->
<!--              </q-tooltip-->
<!--              >-->
<!--            </q-btn>-->
            <q-btn :label="$t('refresh')" icon="refresh" @click="reFresh()">
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ $t("refreshtip") }}
              </q-tooltip
              >
            </q-btn>
            <q-btn label="获取面单" icon="trending_up" @click="get_mian_dan()">
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >获取面单
              </q-tooltip
              >
            </q-btn>
            <q-btn label="批量确认订单" icon="recommend" @click="confirmOrders()">
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >批量确认订单
              </q-tooltip
              >
            </q-btn>
            <q-btn label="全部生成拣货单" icon="confirmation_number" @click="orderreleaseAllData()">
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >全部生成拣货单
              </q-tooltip
              >
            </q-btn>
<!--            <q-btn-->
<!--              v-show="-->
<!--                  $q.localStorage.getItem('staff_type') !== 'Supplier' &&-->
<!--                  $q.localStorage.getItem('staff_type') !== 'Customer' &&-->
<!--                  $q.localStorage.getItem('staff_type') !== 'Inbound' &&-->
<!--                  $q.localStorage.getItem('staff_type') !== 'StockControl'-->
<!--                "-->
<!--              @click="BatchConfirmorderClick"-->
<!--              :label="$t('batch_confirmorder')"-->
<!--              :disable="selected.length === 0"-->
<!--              icon="img:statics/outbound/order.png"-->
<!--            >-->
<!--              <q-tooltip-->
<!--                content-class="bg-amber text-black shadow-4"-->
<!--                :offset="[10, 10]"-->
<!--                content-style="font-size: 12px"-->
<!--              >-->
<!--                {{ $t("batch_confirmorder") }}-->
<!--              </q-tooltip>-->
<!--            </q-btn>-->
<!--            <q-btn-->
<!--              v-show="-->
<!--                $q.localStorage.getItem('staff_type') !== 'Supplier' &&-->
<!--                $q.localStorage.getItem('staff_type') !== 'Customer' &&-->
<!--                $q.localStorage.getItem('staff_type') !== 'Inbound' &&-->
<!--                $q.localStorage.getItem('staff_type') !== 'StockControl'-->
<!--              "-->
<!--              :label="$t('release')"-->
<!--              icon="img:statics/outbound/orderrelease.png"-->
<!--              @click="orderreleaseAllData()"-->
<!--            >-->
<!--              <q-tooltip-->
<!--                content-class="bg-amber text-black shadow-4"-->
<!--                :offset="[10, 10]"-->
<!--                content-style="font-size: 12px"-->
<!--              >{{ $t("releaseallorder") }}-->
<!--              </q-tooltip-->
<!--              >-->
<!--            </q-btn>-->

<!--            <q-btn-->
<!--              v-if="isVip9 === 9"-->
<!--              @click="uploadVisible = true"-->
<!--              :label="$t('upload_center.upload')"-->
<!--              icon="file_upload"-->
<!--            >-->
<!--              <q-tooltip-->
<!--                content-class="bg-amber text-black shadow-4"-->
<!--                :offset="[10, 10]"-->
<!--                content-style="font-size: 12px"-->
<!--              >-->
<!--                {{ $t("upload_center.uploadfiles") }}-->
<!--              </q-tooltip>-->
<!--            </q-btn>-->

            <q-btn
              label='下载拣货单'
              icon="file_download"
              @click="handleDownLoadAllData"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >
                下载所有拣货单
              </q-tooltip>
            </q-btn>
          </q-btn-group>
          <q-input
            v-model="filterData.txnid"
            filled
            autogrow
            label="TxnId"
          />
          <q-select v-model="filterData.order_type" outlined :options="order_type_list" label="发货方式" style="width: 150px"/>
          <q-select v-model="filterData.order_line" outlined :options="order_line_list" label="订单行" style="width: 150px"/>
          <q-select v-model="filterData.carrier" outlined :options="carrier_list" label="承运人" style="width: 150px"/>
          <q-input
            v-model="filterData.sku"
            filled
            autogrow
            label="SKU"
            style="width: 150px"
          />
          <q-btn label="筛选" @click="sortData()"></q-btn>
          <q-btn label="清空" @click="filterDataClear()"></q-btn>
<!--          <q-input-->
<!--            outlined-->
<!--            rounded-->
<!--            dense-->
<!--            debounce="300"-->
<!--            color="primary"-->
<!--            v-model="filter"-->
<!--            :placeholder="$t('search')"-->
<!--            @blur="getSearchList()"-->
<!--            @keyup.enter="getSearchList()"-->
<!--          >-->
<!--            <template v-slot:append>-->
<!--              <q-icon name="search" @click="getSearchList()"/>-->
<!--            </template>-->
<!--          </q-input>-->
        </template>
        <template v-slot:body-cell-action="props">
          <q-td key="action" :props="props" style="width: 100px">
            <q-btn
              v-show="props.row.mian_dan !== ''"
              round
              flat
              push
              color="red"
              icon="visibility"
              @click="openPdf(props.row.txnid)"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >已经获得面单
              </q-tooltip
              >
            </q-btn>
            <q-btn
              v-show="props.row.mian_dan === ''"
              round
              flat
              push
              color="grey"
              icon="visibility"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >还没有拿到面单
              </q-tooltip
              >
            </q-btn>
            <q-btn
              v-show="
                $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                $q.localStorage.getItem('staff_type') !== 'Customer' &&
                $q.localStorage.getItem('staff_type') !== 'Inbound' &&
                $q.localStorage.getItem('staff_type') !== 'StockControl'
              "
              round
              flat
              push
              color="positive"
              icon="img:statics/outbound/order.png"
              @click="neworderData(props.row)"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ $t("confirmorder") }}
              </q-tooltip
              >
            </q-btn>
<!--            <q-btn-->
<!--              v-show="-->
<!--                $q.localStorage.getItem('staff_type') !== 'Supplier' &&-->
<!--                $q.localStorage.getItem('staff_type') !== 'Customer' &&-->
<!--                $q.localStorage.getItem('staff_type') !== 'Inbound' &&-->
<!--                $q.localStorage.getItem('staff_type') !== 'StockControl'-->
<!--              "-->
<!--              round-->
<!--              flat-->
<!--              push-->
<!--              color="positive"-->
<!--              icon="img:statics/outbound/orderrelease.png"-->
<!--              @click="orderreleaseData(props.row)"-->
<!--            >-->
<!--              <q-tooltip-->
<!--                content-class="bg-amber text-black shadow-4"-->
<!--                :offset="[10, 10]"-->
<!--                content-style="font-size: 12px"-->
<!--              >{{ $t("releaseorder") }}-->
<!--              </q-tooltip-->
<!--              >-->
<!--            </q-btn>-->
            <!-- <q-btn
              round
              flat
              push
              color="secondary"
              icon="file_download"
              @click="handleRecordDownload(props.row)"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
                >{{ $t("twoKai.deliver_download") }}</q-tooltip
              >
            </q-btn> -->
            <q-btn
              v-show="
                $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                $q.localStorage.getItem('staff_type') !== 'Customer' &&
                $q.localStorage.getItem('staff_type') !== 'Inbound' &&
                $q.localStorage.getItem('staff_type') !== 'StockControl'
              "
              round
              flat
              push
              color="secondary"
              icon="article"
              @click="PrintPickingList(props.row)"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ $t("twoKai.look_jianhuodan") }}
              </q-tooltip
              >
            </q-btn>
            <q-btn
              v-show="
                $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                $q.localStorage.getItem('staff_type') !== 'Customer' &&
                $q.localStorage.getItem('staff_type') !== 'Inbound' &&
                $q.localStorage.getItem('staff_type') !== 'StockControl'
              "
              round
              flat
              push
              color="purple"
              icon="img:statics/outbound/picked.png"
              @click="pickedData(props.row)"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ $t("confirmpicked") }}
              </q-tooltip
              >
            </q-btn>
            <q-btn
              v-show="
                $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                $q.localStorage.getItem('staff_type') !== 'Customer' &&
                $q.localStorage.getItem('staff_type') !== 'Inbound' &&
                $q.localStorage.getItem('staff_type') !== 'StockControl'
              "
              round
              flat
              push
              color="dark"
              icon="rv_hookup"
              @click="DispatchDN(props.row)"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
                >{{ $t("dispatch") }}</q-tooltip
              >
            </q-btn>
            <!-- <q-btn
              v-show="
                $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                $q.localStorage.getItem('staff_type') !== 'Customer' &&
                $q.localStorage.getItem('staff_type') !== 'Inbound' &&
                $q.localStorage.getItem('staff_type') !== 'StockControl'
              "
              round
              flat
              push
              color="info"
              icon="img:statics/outbound/receiving.png"
              @click="PODData(props.row)"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
                >{{ $t("outbound.pod") }}</q-tooltip
              >
            </q-btn> -->
            <q-btn
              v-show="
                $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                $q.localStorage.getItem('staff_type') !== 'Customer' &&
                $q.localStorage.getItem('staff_type') !== 'Inbound' &&
                $q.localStorage.getItem('staff_type') !== 'StockControl'
              "
              round
              flat
              push
              color="purple"
              icon="edit"
              @click="editData(props.row)"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ $t("edit") }}
              </q-tooltip
              >
            </q-btn>
            <q-btn
              v-show="
                $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                $q.localStorage.getItem('staff_type') !== 'Customer' &&
                $q.localStorage.getItem('staff_type') !== 'Inbound' &&
                $q.localStorage.getItem('staff_type') !== 'StockControl' &&
                $q.localStorage.getItem('is_vip') === 9
              "
              round
              flat
              push
              color="dark"
              icon="delete"
              @click="deleteData(props.row)"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ $t("delete") }}
              </q-tooltip
              >
            </q-btn>
            <q-btn
              round
              flat
              push
              color="dark"
              icon="privacy_tip"
              @click="commentsData(props.row)"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ props.row.comments }}
              </q-tooltip
              >
            </q-btn>
          </q-td>
          <template v-if="props.row.transportation_fee.detail !== []">
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >
                <q-list>
                  <div
                    v-for="(transportation_fee, index) in props.row
                      .transportation_fee.detail"
                    :key="index"
                  >
                    <q-item v-ripple>
                      <q-item-section>
                        <q-item-label>{{
                            transportation_fee.transportation_supplier
                          }}
                        </q-item-label>
                        <q-item-label
                        >{{ $t("estimate") }}:
                          {{
                            transportation_fee.transportation_cost
                          }}
                        </q-item-label
                        >
                      </q-item-section>
                    </q-item>
                  </div>
                </q-list>
              </q-tooltip>
            </template>
        </template>
      </q-table>
    </transition>
    <template>
      <div class="q-pa-lg flex flex-center">
        <q-select outlined v-model="max_page_data" :options="max_page" label="每页数量" style="width: 200px" />
        <q-btn
          v-show="page_count===0"
          flat
          push
          color="dark"
          :label="$t('no_data')"
        ></q-btn>
        <q-pagination
          v-show="page_count!==0"
          v-model="current"
          color="purple"
          :max="Math.ceil(page_count / 1000 ) "
          :max-pages="1000"
          boundary-numbers
          direction-links
          @click="getList()"
        />
      </div>
    </template>
    <q-dialog v-model="newForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ newFormData.dn_code }}</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-select
            filled
            use-input
            fill-input
            hide-selected
            input-debounce="0"
            dense
            outlined
            square
            v-model="newFormData.customer"
            :options="customer_list"
            @filter="filterFnS"
            @input-value="setModel"
            :label="$t('baseinfo.view_customer.customer_name')"
            style="margin-bottom: 5px"
            :rules="[(val) => (val && val.length > 0) || error1]"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:Sno-option>
              <q-item>
                <q-item-section class="text-grey"> No Result</q-item-section>
              </q-item>
            </template>
          </q-select>

          <q-select
            dense
            outlined
            square
            emit-value
            map-options
            v-model="warehouseId"
            option-value="id"
            option-label="warehosue_name"
            :options="warehouse_list"
            :label="$t('twoKai.view_warehouse.warehouse_name')"
            :rules="[(val) => val || $t('twoKai.view_warehouse.error1')]"
          />

          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData1.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData1.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(1)"
                @input-value="setOptions"
                @filter="filterFn"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item
                  >
                    <q-item-section class="text-grey"
                    >No results
                    </q-item-section
                    >
                  </q-item
                  >
                </template>
                <template v-if="goodsData1.code" v-slot:append>
                  <q-icon
                    name="cancel"
                    @click.stop="goodsData1.code = ''"
                    class="cursor-pointer"
                  />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData2.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData2.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(2)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item
                  >
                    <q-item-section class="text-grey"
                    >No results
                    </q-item-section
                    >
                  </q-item
                  >
                </template>
                <template v-if="goodsData2.code" v-slot:append>
                  <q-icon
                    name="cancel"
                    @click.stop="goodsData2.code = ''"
                    class="cursor-pointer"
                  />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData3.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData3.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(3)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item
                  >
                    <q-item-section class="text-grey"
                    >No results
                    </q-item-section
                    >
                  </q-item
                  >
                </template>
                <template v-if="goodsData3.code" v-slot:append>
                  <q-icon
                    name="cancel"
                    @click.stop="goodsData3.code = ''"
                    class="cursor-pointer"
                  />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData4.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData4.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(4)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item
                  >
                    <q-item-section class="text-grey"
                    >No results
                    </q-item-section
                    >
                  </q-item
                  >
                </template>
                <template v-if="goodsData4.code" v-slot:append>
                  <q-icon
                    name="cancel"
                    @click.stop="goodsData4.code = ''"
                    class="cursor-pointer"
                  />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData5.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData5.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(5)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item
                  >
                    <q-item-section class="text-grey"
                    >No results
                    </q-item-section
                    >
                  </q-item
                  >
                </template>
                <template v-if="goodsData5.code" v-slot:append>
                  <q-icon
                    name="cancel"
                    @click.stop="goodsData5.code = ''"
                    class="cursor-pointer"
                  />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData6.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData6.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(6)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item
                  >
                    <q-item-section class="text-grey"
                    >No results
                    </q-item-section
                    >
                  </q-item
                  >
                </template>
                <template v-if="goodsData6.code" v-slot:append>
                  <q-icon
                    name="cancel"
                    @click.stop="goodsData6.code = ''"
                    class="cursor-pointer"
                  />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData7.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData7.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(7)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item
                  >
                    <q-item-section class="text-grey"
                    >No results
                    </q-item-section
                    >
                  </q-item
                  >
                </template>
                <template v-if="goodsData7.code" v-slot:append>
                  <q-icon
                    name="cancel"
                    @click.stop="goodsData7.code = ''"
                    class="cursor-pointer"
                  />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData8.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData8.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(8)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item
                  >
                    <q-item-section class="text-grey"
                    >No results
                    </q-item-section
                    >
                  </q-item
                  >
                </template>
                <template v-if="goodsData8.code" v-slot:append>
                  <q-icon
                    name="cancel"
                    @click.stop="goodsData8.code = ''"
                    class="cursor-pointer"
                  />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData9.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData9.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(9)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item
                  >
                    <q-item-section class="text-grey"
                    >No results
                    </q-item-section
                    >
                  </q-item
                  >
                </template>
                <template v-if="goodsData9.code" v-slot:append>
                  <q-icon
                    name="cancel"
                    @click.stop="goodsData9.code = ''"
                    class="cursor-pointer"
                  />
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData10.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData10.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(10)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item
                  >
                    <q-item-section class="text-grey"
                    >No results
                    </q-item-section
                    >
                  </q-item
                  >
                </template>
                <template v-if="goodsData10.code" v-slot:append>
                  <q-icon
                    name="cancel"
                    @click.stop="goodsData10.code = ''"
                    class="cursor-pointer"
                  />
                </template>
              </q-select>
            </template>
          </q-input>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="isEdit ? editDataCancel() : newDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn
            color="primary"
            @click="isEdit ? editDataSubmit() : newDataSubmit()"
          >{{ $t("submit") }}
          </q-btn
          >
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="deleteForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ $t("delete") }}</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section
          style="max-height: 325px; width: 400px"
          class="scroll"
        >{{ $t("deletetip") }}
        </q-card-section
        >
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="deleteDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="deleteDataSubmit()">{{
              $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="commentsForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>备注</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section
          style="max-height: 325px; width: 400px"
          class="scroll"
        >
          <q-input v-model="commentsDetail" label="备注"></q-input>
        </q-card-section
        >
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="commentsDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="commentsDataSubmit()">{{
              $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="neworderForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ $t("confirmorder") }}</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section
          style="max-height: 325px; width: 400px"
          class="scroll"
        >{{ $t("deletetip") }}
        </q-card-section
        >
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="neworderDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="neworderDataSubmit()">{{
              $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="neworderListForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ $t("confirmorder") }}</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section
          style="max-height: 325px; width: 400px"
          class="scroll"
        >{{ $t("deletetip") }}
        </q-card-section
        >
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="neworderListDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="neworderListDataSubmit()">{{
              $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="orderreleaseForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ $t("releaseorder") }}</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section
          style="max-height: 325px; width: 400px"
          class="scroll"
        >{{ $t("deletetip") }}
        </q-card-section
        >
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="orderreleaseDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="orderreleaseDataSubmit()">{{
              $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="viewForm">
        <q-pdfviewer
          v-model="show"
          type="pdfjs"
          :src="updatedSrc"
          content-class="absolute"
        />
    </q-dialog>
    <q-dialog v-model="viewPLForm">
      <q-card id="printPL">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ $t("twoKai.look_jianhuodan") }}</div>
          <q-space/>
        </q-bar>
        <div class="col-4" style="margin-top: 5%">
          <img :src="bar_code" style="width: 21%; margin-left: 70%"/>
        </div>
        <q-markup-table>
          <thead>
          <tr>
            <th class="text-left">{{ $t("outbound.view_dn.dn_code") }}</th>

            <th class="text-right">
              {{ $t("warehouse.view_binset.bin_name") }}
            </th>
            <th class="text-left">SKU</th>
            <!-- <th class="text-right">{{ $t("outbound.view_dn.goods_qty") }}</th> -->
            <th class="text-right">{{ $t("outbound.pickstock") }}</th>
            <th class="text-right">{{ $t("outbound.pickedstock") }}</th>
            <th class="text-right">Comments</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(view, index) in pickinglist_print_table" :key="index">
            <td class="text-left">{{ view.txnid }}</td>
            <td class="text-left">{{ view.order_type }}</td>
            <td class="text-left">{{ view.dn_code }}</td>

            <td class="text-right">{{ view.bin_name }}</td>
            <td class="text-left">{{ view.goods_code }}</td>
            <!--  <td class="text-right">{{ view.pick_qty }}</td> -->
            <td class="text-right">{{ view.pick_qty }}</td>
            <td class="text-right" v-show="picklist_check === 0">
              {{ view.picked_qty }}
            </td>
            <td class="text-right" v-show="picklist_check > 0">
              {{ view.picked_qty }}
            </td>
            <td class="text-right"></td>
          </tr>
          </tbody>
        </q-markup-table>
      </q-card>
      <!--  <div style="float: right; padding: 15px 15px 15px 0">
        <q-btn color="primary" icon="print" v-print="printPL">print</q-btn>
      </div> -->
    </q-dialog>
    <q-dialog v-model="pickedForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ pickFormData.dn_code }}</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-input
            dense
            outlined
            square
            debounce="500"
            disable
            readonly
            v-model="pickFormData.customer"
            :label="$t('baseinfo.view_customer.customer_name')"
            style="margin-bottom: 5px"
          />
          <div v-for="(item, index) in pickFormData.goodsData" :key="index">
            <q-input
              dense
              outlined
              square
              bottom-slots
              type="number"
              v-model="item.pick_qty"
              :label="item.goods_code"
            >
              <template v-slot:append>
                {{ item.bin_name }}
              </template>
            </q-input>
          </div>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="pickedDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="pickedDataSubmit()">{{
              $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="dispatchForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ dispatchFormData.dn_code }}</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-select
            dense
            outlined
            square
            use-input
            hide-selected
            fill-input
            v-model="dispatchFormData.driver"
            :label="$t('driver.view_driver.driver_name')"
            :options="driver_options"
            @filter="filterFnDispatch"
            autofocus
            @keyup.enter="dispatchDataSubmit()"
          >
            <template v-slot:no-option>
              <q-item
              >
                <q-item-section class="text-grey"
                >No results
                </q-item-section
                >
              </q-item
              >
            </template>
            <template v-if="dispatchFormData.driver" v-slot:append>
              <q-icon
                name="cancel"
                @click.stop="dispatchFormData.driver = ''"
                class="cursor-pointer"
              />
            </template>
          </q-select>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="dispatchDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="dispatchDataSubmit()">{{
              $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="podForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ $t("outbound.dn") }}: {{ podFormData.dn_code }}</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          {{ $t("baseinfo.customer") }}: {{ podFormData.customer }}
          <div v-for="(item, index) in podFormData.goodsData" :key="index">
            <q-input
              dense
              outlined
              square
              debounce="500"
              v-model.number="item.intransit_qty"
              type="number"
              :label="$t('outbound.view_dn.delivery_actual_qty')"
              style="margin-bottom: 5px"
              :error-message="error2"
              :error="isError1"
              :rules="[validate1]"
            >
              <template v-slot:after>
                <q-input
                  dense
                  outlined
                  square
                  debounce="500"
                  v-model.number="item.delivery_damage_qty"
                  type="number"
                  :label="$t('outbound.view_dn.delivery_damage_qty')"
                  style="margin-top: 11%"
                  :error-message="error2"
                  :error="isError2"
                  :rules="[
                    validate2(item.delivery_damage_qty, item.intransit_qty),
                  ]"
                ></q-input>
              </template>
            </q-input>
          </div>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="PODDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="PODDataSubmit()">{{
              $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>

    <q-dialog v-model="uploadVisible">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ $t("twoKai.upload_asn.title") }}</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
                $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-uploader
            :url="goodslistfile_pathname"
            method="post"
            :headers="[
              { name: 'token', value: token },
              { name: 'language', value: lang },
              { name: 'operator', value: login_id },
            ]"
            :field-name="(file) => 'file'"
            @rejected="onRejected"
            @added="getfileinfo"
            @finish="handleUploadFinish"
            class="custom-uploader"
            auto-upload
          >
            <template v-slot:header="scope">
              <q-btn
                type="a"
                :label="$t('upload_center.upload')"
                icon="file_upload"
                @click="scope.pickFiles"
                round
                dense
                flat
              >
                <q-uploader-add-trigger/>
                <q-tooltip
                  content-class="bg-amber text-black shadow-4"
                  :offset="[10, 10]"
                  content-style="font-size: 12px"
                >{{ $t("upload_center.uploadfiles") }}
                </q-tooltip
                >
              </q-btn>
            </template>
          </q-uploader>

          <p class="custom-download">
            <span @click="handleDownloadTemplate">
              {{ $t("twoKai.upload_asn.template") }}</span
            >
          </p>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>
<router-view/>

<script>
import {
  baseurl,
  getauth,
  getfile,
  postauth,
  putauth,
  deleteauth,
  ViewPrintAuth
} from 'boot/axios_request'
import { date, exportFile, LocalStorage, openURL } from 'quasar'

export default {
  name: 'Pagednlist',
  data () {
    return {
      current: 1,
      page_count: 0,
      uploadVisible: false,
      token: LocalStorage.getItem('openid'),
      lang: LocalStorage.getItem('lang'),
      login_id: LocalStorage.getItem('login_id'),
      isVip9: LocalStorage.getItem('is_vip') || '',
      goodslistfile_pathname: baseurl + 'uploadfile/dnlistfileadd/',
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'dn/',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',
      table_list: [],
      viewprint_table: [],
      bar_code: '',
      pickinglist_print_table: [],
      pickinglist_check: 0,
      warehouse_detail: {},
      customer_list: [],
      customer_list1: [],
      driver_list: [],
      customer_detail: {},
      commentsForm: false,
      commentsID: '',
      commentsDetail: '',
      commentsDic: {},
      columns: [
        {
          name: 'TxnId',
          required: true,
          label: 'TxnId',
          align: 'left',
          field: 'txnid'
        },
        {
          name: 'order_type',
          required: true,
          label: 'Method',
          align: 'left',
          field: 'order_type'
        },
        {
          name: 'trackingnumber',
          required: true,
          label: '面单号',
          align: 'left',
          field: 'trackingnumber'
        },
        {
          name: 'comments',
          label: '备注',
          field: 'comments',
          align: 'center'
        },
        {
          name: 'carrier',
          label: '承运人',
          field: 'carrier',
          align: 'center'
        },
        {
          name: 'dn_status',
          label: this.$t('outbound.view_dn.dn_status'),
          field: 'dn_status',
          align: 'center'
        },
        {
          name: 'warehouse_id',
          label: this.$t('twoKai.warehouse_id'),
          field: 'warehouse_id',
          align: 'center',
          format: (val, row) => {
            return this.switchWarehouse(row)
          }
        },
        {
          name: 'total_weight',
          label: this.$t('outbound.view_dn.total_weight'),
          field: 'total_weight',
          align: 'center',
          format: (val, row) => {
            return row.total_weight.toFixed(4)
          }
        },
        {
          name: 'total_volume',
          label: this.$t('outbound.view_dn.total_volume'),
          field: 'total_volume',
          align: 'center',
          format: (val, row) => {
            return row.total_volume.toFixed(4)
          }
        },
        {
          name: 'customer',
          label: this.$t('outbound.view_dn.customer'),
          field: 'customer',
          align: 'center'
        },
        {
          name: 'creater',
          label: this.$t('creater'),
          field: 'creater',
          align: 'center'
        },
        {
          name: 'create_time',
          label: this.$t('createtime'),
          field: 'create_time',
          align: 'center'
        },
        {
          name: 'update_time',
          label: this.$t('updatetime'),
          field: 'update_time',
          align: 'center'
        },
        { name: 'action', label: this.$t('action'), align: 'right' }
      ],
      filter: '',
      pagination: {
        page: 1,
        rowsPerPage: '1000'
      },
      newForm: false,
      options1: [],
      isEdit: false,
      listNumber: '',
      options: LocalStorage.getItem('goods_code_list'),
      driver_options: LocalStorage.getItem('driver_name_list'),
      newdn: { creater: '' },
      warehouseId: '',
      warehouse_list: [],
      newFormData: {
        dn_code: '',
        customer: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      },
      pickFormData: {
        dn_code: '',
        customer: '',
        goodsData: [],
        creater: ''
      },
      goodsData1: { bin: '', code: '', qty: '' },
      goodsData2: { bin: '', code: '', qty: '' },
      goodsData3: { bin: '', code: '', qty: '' },
      goodsData4: { bin: '', code: '', qty: '' },
      goodsData5: { bin: '', code: '', qty: '' },
      goodsData6: { bin: '', code: '', qty: '' },
      goodsData7: { bin: '', code: '', qty: '' },
      goodsData8: { bin: '', code: '', qty: '' },
      goodsData9: { bin: '', code: '', qty: '' },
      goodsData10: { bin: '', code: '', qty: '' },
      editid: 0,
      editFormData: {},
      pickedForm: false,
      pickedid: 0,
      deleteForm: false,
      deleteid: 0,
      neworderForm: false,
      neworderid: 0,
      orderreleaseForm: false,
      orderreleaseid: 0,
      viewForm: false,
      viewPLForm: false,
      viewdn: '',
      viewid: 0,
      dispatchid: 0,
      dispatchForm: false,
      dispatchFormData: {
        dn_code: '',
        driver: ''
      },
      podid: 0,
      podForm: false,
      podFormData: {
        dn_code: '',
        customer: '',
        goodsData: []
      },
      printObj: {
        id: 'printMe',
        popTitle: this.$t('outbound.dn')
      },
      printPL: {
        id: 'printPL',
        popTitle: this.$t('outbound.pickinglist')
      },
      error1: this.$t('baseinfo.view_customer.error1'),
      error2: this.$t('notice.valerror'),
      isError1: false,
      isError2: false,
      selected: [],
      neworderidList: [],
      neworderListForm: false,
      show: true,
      src: 'media/miandan/',
      max_page_data: 30,
      max_page: [30, 100, 500, 1000],
      filterDataForm: false,
      filterData: {
        txnid: '',
        order_type: '',
        order_line: '',
        carrier: '',
        sku: ''
      },
      order_type_list: [],
      order_line_list: ['单件', '多件'],
      carrier_list: [],
      txnid_list_data: [],
      order_type_data: '',
      order_line: '',
      carrier_data: '',
      sku_list_data: []
    }
  },
  computed: {
    updatedSrc () {
      if (process.env.MODE === 'electron') {
        return '/' + this.src
      }
      return this.getLocation(this.src)
    }
  },
  methods: {
    pickingOrders () {
      console.log(111)
    },
    sortData () {
      var _this = this
      if (this.filterData.txnid !== '') {
        if (this.filterData.txnid.includes(',')) {
          var split_txnid = ''
          split_txnid = this.filterData.txnid.split(',')
          _this.txnid_list_data = []
          split_txnid.forEach(item => {
            if (item !== '') {
              _this.txnid_list_data.push(item)
            }
          })
        } else {
          _this.txnid_list_data = []
          _this.txnid_list_data.push(this.filterData.txnid)
        }
      } else {
        _this.txnid_list_data = []
      }
      if (this.filterData.sku !== '') {
        if (this.filterData.sku.includes(',')) {
          var split_sku = ''
          split_sku = this.filterData.sku.split(',')
          _this.sku_list_data = []
          split_sku.forEach(item => {
            if (item !== '') {
              _this.sku_list_data.push(item)
            }
          })
        } else {
          _this.sku_list_data = []
          _this.sku_list_data.push(this.filterData.sku)
        }
      } else {
        _this.sku_list_data = []
      }
      this.order_type_data = this.filterData.order_type
      this.order_line = this.filterData.order_line
      this.carrier_data = this.filterData.carrier
      _this.getList()
    },
    filterDataClear () {
      this.filterData = {
        txnid: [],
        order_type: '',
        order_line: '',
        carrier: '',
        sku: []
      }
    },
    confirmOrders () {
      var _this = this
      postauth(_this.pathname + 'confirmorders/', {})
        .then((res) => {
          this.$q.notify({
            message: '确认订单完成',
            color: 'green',
            icon: 'check'
          })
          this.getList()
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    get_mian_dan () {
      var _this = this
      postauth(_this.pathname + 'getmiandan/', _this.filterData)
        .then((res) => {
          _this.$q.notify({
            message: '获取面单结束',
            color: 'green',
            icon: 'check'
          })
          _this.getList()
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    handleRecordDownload (record) {
      if (!record.id) {
        this.$q.notify({
          message: 'Browser denied file download...',
          color: 'negative',
          icon: 'warning'
        })
        return
      }

      if (LocalStorage.has('auth')) {
        getfile(
          `dn/filedetail/${record.id}/?lang=${LocalStorage.getItem('lang')}`
        ).then((res) => {
          var timeStamp = Date.now()
          var formattedString = date.formatDate(timeStamp, 'YYYYMMDDHHmmssSSS')
          const status = exportFile(
            `dn_filedetail_${record.id}_${formattedString}.csv`,
            '\uFEFF' + res.data,
            'text/csv'
          )
          if (status !== true) {
            this.$q.notify({
              message: 'Browser denied file download...',
              color: 'negative',
              icon: 'warning'
            })
          }
        })
      } else {
        this.$q.notify({
          message: this.$t('notice.loginerror'),
          color: 'negative',
          icon: 'warning'
        })
      }
    },
    handleDownLoadAllData () {
      var _this = this
      var txnid_search = this.txnid_list_data
      var order_type_search = this.order_type_data
      var order_line_search = this.order_line
      var carrier_search = this.carrier_data
      var sku_search = this.sku_list_data
      if (LocalStorage.has('auth')) {
        getfile(
          `dn/picklistdownload/?lang=${LocalStorage.getItem('lang') + '&txnid__in=' + txnid_search + '&order_type=' + order_type_search + '&carrier=' + carrier_search + '&sku_search__in=' + sku_search + '&order_line=' + order_line_search, {}}`
        ).then((res) => {
          var timeStamp = Date.now()
          var formattedString = date.formatDate(timeStamp, 'YYYYMMDDHHmmssSSS')
          const status = exportFile(
            `dn_picklist_${formattedString}.csv`,
            '\uFEFF' + res.data,
            'text/csv'
          )
          if (status !== true) {
            this.$q.notify({
              message: 'Browser denied file download...',
              color: 'negative',
              icon: 'warning'
            })
          } else {
            this.$q.notify({
              message: '下载完成',
              color: 'green',
              icon: 'check'
            })
          }
        })
      } else {
        this.$q.notify({
          message: this.$t('notice.loginerror'),
          color: 'negative',
          icon: 'warning'
        })
      }
    },
    onRejected (rejectedEntries) {
      this.$q.notify({
        type: 'negative',
        message: `${rejectedEntries.length} file(s) did not pass validation constraints`
      })
    },
    getfileinfo (file) {
      console.log(file, '------')
      this.$q.loading.show({ message: '上传中' })
    },
    handleUploadFinish () {
      this.$q.loading.hide()
      this.$q.notify({
        message: 'Success upload',
        icon: 'check',
        color: 'green'
      })
      this.getList()
      this.uploadVisible = false
    },
    handleDownloadTemplate () {
      if (LocalStorage.has('auth')) {
        if (LocalStorage.has('lang')) {
          if (LocalStorage.getItem('lang') === 'zh-hans') {
            openURL(baseurl + 'media/upload_example/dnlist_cn.xlsx')
          } else {
            openURL(baseurl + 'media/upload_example/dnlist_en.xlsx')
          }
        } else {
          openURL(baseurl + 'media/upload_example/dnlist_en.xlsx')
        }
      } else {
        this.$q.notify({
          message: this.$t('notice.loginerror'),
          color: 'negative',
          icon: 'warning'
        })
      }
    },

    switchWarehouse (record) {
      const filterItem = this.warehouse_list.find(
        (item) => (item.warehouse_id = record.warehouse_id)
      )
      return record.warehouse_id + '-' + filterItem.warehosue_name || ''
    },

    validate1 (val) {
      const reg = /^[1-9]\d*$/g
      const check = reg.test(val)
      if (check) {
        this.isError1 = false
      } else {
        this.isError1 = true
      }
    },
    validate2 (val1, val2) {
      const reg = /^[0-9]\d*$/g
      const check = reg.test(val1)
      if (check && val1 <= val2) {
        this.isError2 = false
      } else {
        this.isError2 = true
      }
    },
    getList () {
      var _this = this
      var txnid_search = this.txnid_list_data
      var order_type_search = this.order_type_data
      var order_line_search = this.order_line
      var carrier_search = this.carrier_data
      var sku_search = this.sku_list_data
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname + 'list/' + '?max_page=' + _this.max_page_data + '&page=' + this.current + '&txnid__in=' + txnid_search + '&order_type=' + order_type_search + '&carrier=' + carrier_search + '&sku_search__in=' + sku_search + '&order_line=' + order_line_search, {})
          .then((res) => {
            _this.page_count = res.count
            _this.table_list = []
            res.results.forEach((item) => {
              if (item.dn_status === 1) {
                item.dn_status = _this.$t('outbound.freshorder')
              } else if (item.dn_status === 2) {
                item.dn_status = _this.$t('outbound.neworder')
              } else if (item.dn_status === 3) {
                item.dn_status = _this.$t('outbound.pickstock')
              } else if (item.dn_status === 4) {
                item.dn_status = _this.$t('outbound.pickedstock')
              } else if (item.dn_status === 5) {
                item.dn_status = _this.$t('outbound.shippedstock')
              } else if (item.dn_status === 6) {
                item.dn_status = _this.$t('outbound.received')
              } else {
                item.dn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            res.results.forEach((item) => {
              if (item.asn_status === 1) {
                item.asn_status = _this.$t()
              }
            })
            _this.customer_list = res.customer_list
            _this.customer_list1 = res.customer_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
            _this.warehouse_list = res.warehouse_list
            _this.order_type_list = res.order_type_list
            _this.carrier_list = res.carrier_list
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    getSearchList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        var xxx = ['ZD-11386','ZD-10147']
        getauth(_this.pathname + 'list/?max_page=' + _this.max_page_data + '&txnid__in=' + xxx + '&page=' + this.current, {})
          .then((res) => {
            _this.table_list = []
            _this.page_count = res.count
            res.results.forEach((item) => {
              if (item.dn_status === 1) {
                item.dn_status = _this.$t('outbound.freshorder')
              } else if (item.dn_status === 2) {
                item.dn_status = _this.$t('outbound.neworder')
              } else if (item.dn_status === 3) {
                item.dn_status = _this.$t('outbound.pickstock')
              } else if (item.dn_status === 4) {
                item.dn_status = _this.$t('outbound.pickedstock')
              } else if (item.dn_status === 5) {
                item.dn_status = _this.$t('outbound.shippedstock')
              } else if (item.dn_status === 6) {
                item.dn_status = _this.$t('outbound.received')
              } else {
                item.dn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.customer_list = res.customer_list
            _this.customer_list1 = res.customer_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    getListPrevious () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname_previous, {})
          .then((res) => {
            _this.table_list = []
            res.results.forEach((item) => {
              if (item.dn_status === 1) {
                item.dn_status = _this.$t('outbound.freshorder')
              } else if (item.dn_status === 2) {
                item.dn_status = _this.$t('outbound.neworder')
              } else if (item.dn_status === 3) {
                item.dn_status = _this.$t('outbound.pickstock')
              } else if (item.dn_status === 4) {
                item.dn_status = _this.$t('outbound.pickedstock')
              } else if (item.dn_status === 5) {
                item.dn_status = _this.$t('outbound.shippedstock')
              } else if (item.dn_status === 6) {
                item.dn_status = _this.$t('outbound.received')
              } else {
                item.dn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.customer_list = res.customer_list
            _this.customer_list1 = res.customer_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    getListNext () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname_next, {})
          .then((res) => {
            _this.table_list = []
            res.results.forEach((item) => {
              if (item.dn_status === 1) {
                item.dn_status = _this.$t('outbound.freshorder')
              } else if (item.dn_status === 2) {
                item.dn_status = _this.$t('outbound.neworder')
              } else if (item.dn_status === 3) {
                item.dn_status = _this.$t('outbound.pickstock')
              } else if (item.dn_status === 4) {
                item.dn_status = _this.$t('outbound.pickedstock')
              } else if (item.dn_status === 5) {
                item.dn_status = _this.$t('outbound.shippedstock')
              } else if (item.dn_status === 6) {
                item.dn_status = _this.$t('outbound.received')
              } else {
                item.dn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.customer_list = res.customer_list
            _this.customer_list1 = res.customer_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    reFresh () {
      var _this = this
      _this.table_list = []
      _this.getList()
    },
    newFormOpen () {
      var _this = this
      _this.isEdit = false
      _this.goodsDataClear()
      _this.newForm = true
      _this.newdn.creater = _this.login_name
      postauth(_this.pathname + 'list/', _this.newdn)
        .then((res) => {
          if (!res.detail) {
            _this.newFormData.dn_code = res.dn_code
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    newDataSubmit () {
      var _this = this
      _this.newFormData.creater = _this.login_name
      let cancelRequest = false
      if (_this.newFormData.customer !== '') {
        _this.newFormData.goods_code = []
        _this.newFormData.goods_qty = []
        let goodsDataCheck = 0
        for (let i = 0; i < 10; i++) {
          const goodsData = `goodsData${i + 1}`
          if (_this[goodsData].code !== '' && _this[goodsData].qty !== '') {
            if (_this[goodsData].qty < 1) {
              cancelRequest = true
              _this.$q.notify({
                message: 'Total Quantity Must Be > 0',
                icon: 'close',
                color: 'negative'
              })
            } else {
              _this.newFormData.goods_code.push(_this[goodsData].code)
              _this.newFormData.goods_qty.push(_this[goodsData].qty)
            }
            goodsDataCheck += 1
          }
        }
        if (goodsDataCheck === 0) {
          cancelRequest = true
          _this.$q.notify({
            message: 'Please Enter The Goods & Qty',
            icon: 'close',
            color: 'negative'
          })
        }
      } else {
        cancelRequest = true
        _this.$q.notify({
          message: 'Please Enter The Customer',
          icon: 'close',
          color: 'negative'
        })
      }
      if (!cancelRequest) {
        postauth(_this.pathname + 'detail/', {
          ..._this.newFormData,
          warehouse_id: _this.warehouseId
        })
          .then((res) => {
            _this.table_list = []
            _this.getList()
            _this.newDataCancel()
            if (res.detail === 'success') {
              _this.$q.notify({
                message: 'Success Create',
                icon: 'check',
                color: 'green'
              })
            }
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      }
    },
    newDataCancel () {
      var _this = this
      _this.newForm = false
      _this.newFormData = {
        dn_code: '',
        customer: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    goodsDataClear () {
      var _this = this
      for (let i = 1; i <= 10; i++) {
        _this[`goodsData${i}`] = { code: '', qty: '' }
      }
    },
    handleSelection ({ rows, added, evt }) {
      // ignore selection change from header of not from a direct click event
      if (rows.length !== 1 || evt === void 0) {
        return
      }

      const { oldSelectedRow } = this
      const [newSelectedRow] = rows
      const { ctrlKey, shiftKey } = evt

      if (shiftKey !== true) {
        this.oldSelectedRow = newSelectedRow
      }

      // wait for the default selection to be performed
      this.$nextTick(() => {
        if (shiftKey === true) {
          const tableRows = this.$refs.table.filteredSortedRows
          let firstIndex = tableRows.indexOf(oldSelectedRow)
          let lastIndex = tableRows.indexOf(newSelectedRow)

          if (firstIndex < 0) {
            firstIndex = 0
          }

          if (firstIndex > lastIndex) {
            [firstIndex, lastIndex] = [lastIndex, firstIndex]
          }

          const rangeRows = tableRows.slice(firstIndex, lastIndex + 1)

          this.selected = added === true
            ? this.selected.concat(rangeRows.filter(row => this.selected.includes(row) === false))
            : this.selected.filter(row => rangeRows.includes(row) === false)
        } else if (ctrlKey !== true && added === true) {
          this.selected = [newSelectedRow]
        }
      })
    },
    editData (e) {
      var _this = this
      _this.isEdit = true
      _this.goodsDataClear()
      if (e.dn_status !== _this.$t('outbound.freshorder')) {
        _this.$q.notify({
          message:
            e.dn_code + ' DN Status Not ' + _this.$t('outbound.freshorder'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.newFormData.dn_code = e.dn_code
        _this.newFormData.customer = e.customer
        _this.warehouseId = e.warehouse_id
        getauth(_this.pathname + 'detail/?dn_code=' + e.dn_code).then((res) => {
          _this.newForm = true
          _this.editid = e.id
          res.results.forEach((detail, index) => {
            _this[`goodsData${index + 1}`] = {
              code: detail.goods_code,
              qty: detail.goods_qty
            }
          })
        })
      }
    },
    editDataSubmit () {
      var _this = this
      _this.newFormData.creater = _this.login_name
      let cancelRequest = false
      if (_this.newFormData.customer !== '') {
        _this.newFormData.goods_code = []
        _this.newFormData.goods_qty = []
        let goodsDataCheck = 0
        for (let i = 0; i < 10; i++) {
          const goodsData = `goodsData${i + 1}`
          if (_this[goodsData].code !== '' && _this[goodsData].qty !== '') {
            if (_this[goodsData].qty < 1) {
              cancelRequest = true
              _this.$q.notify({
                message: 'Total Quantity Must Be > 0',
                icon: 'close',
                color: 'negative'
              })
            } else {
              _this.newFormData.goods_code.push(_this[goodsData].code)
              _this.newFormData.goods_qty.push(_this[goodsData].qty)
            }
            goodsDataCheck += 1
          }
        }
        if (goodsDataCheck === 0) {
          cancelRequest = true
          _this.$q.notify({
            message: 'Please Enter The Goods & Qty',
            icon: 'close',
            color: 'negative'
          })
        }
      } else {
        cancelRequest = true
        _this.$q.notify({
          message: 'Please Enter The Customer',
          icon: 'close',
          color: 'negative'
        })
      }
      if (!cancelRequest) {
        putauth(_this.pathname + 'detail/', {
          ..._this.newFormData,
          warehouse_id: _this.warehouseId
        })
          .then((res) => {
            _this.table_list = []
            _this.editDataCancel()
            _this.getList()
            if (!res.detail) {
              _this.$q.notify({
                message: 'Success Edit DN',
                icon: 'check',
                color: 'green'
              })
            }
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      }
    },
    editDataCancel () {
      var _this = this
      _this.newForm = false
      _this.editid = 0
      _this.warehouseId = ''
      _this.newFormData = {
        dn_code: '',
        customer: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    deleteData (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.freshorder')) {
        _this.$q.notify({
          message:
            e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.freshorder'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.deleteForm = true
        _this.deleteid = e.id
      }
    },
    deleteDataSubmit () {
      var _this = this
      deleteauth(_this.pathname + 'list/' + _this.deleteid + '/')
        .then((res) => {
          _this.table_list = []
          _this.deleteDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Delete DN',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    deleteDataCancel () {
      var _this = this
      _this.deleteForm = false
      _this.deleteid = 0
    },
    commentsData (e) {
      var _this = this
      _this.commentsForm = true
      _this.commentsID = e.id
      _this.commentsDetail = e.comments
      _this.commentsDic = e
    },
    commentsDataSubmit () {
      var _this = this
      this.commentsDic.comments = _this.commentsDetail
      postauth(_this.pathname + 'comments/' + _this.commentsID + '/', _this.commentsDic)
        .then((res) => {
          _this.table_list = []
          _this.commentsDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Delete DN',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    commentsDataCancel () {
      var _this = this
      _this.commentsForm = false
      _this.commentsID = 0
      _this.commentsDetail = ''
      _this.commentsDic = {}
    },
    neworderData (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.freshorder')) {
        _this.$q.notify({
          message:
            e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.freshorder'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.neworderForm = true
        _this.neworderid = e.id
      }
    },
    neworderDataSubmit () {
      var _this = this
      this.$q.loading.show({ message: '确认中' })
      postauth(_this.pathname + 'neworder/' + _this.neworderid + '/', {})
        .then((res) => {
          _this.table_list = []
          _this.neworderDataCancel()
          _this.getList()
          this.$q.loading.hide()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Confirm DN Delivery',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    neworderDataCancel () {
      var _this = this
      _this.neworderForm = false
      _this.neworderid = 0
    },
    neworderLisyDataCancel () {
      var _this = this
      _this.neworderListForm = false
      _this.neworderidList = []
    },
    orderreleaseData (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.neworder')) {
        _this.$q.notify({
          message:
            e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.neworder'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.orderreleaseForm = true
        _this.orderreleaseid = e.id
      }
    },
    orderreleaseAllData () {
      var _this = this
      // this.$q.loading.show({ message: '确认中' })
      postauth(_this.pathname + 'orderrelease/', {})
        .then((res) => {
          _this.table_list = []
          _this.getList()
          _this.$q.notify({
            message: '全部生成拣货单成功',
            icon: 'check',
            color: 'green'
          })
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    orderreleaseDataSubmit () {
      var _this = this
      this.$q.loading.show({ message: '拣货单生成中' })
      putauth(_this.pathname + 'orderrelease/' + _this.orderreleaseid + '/', {})
        .then((res) => {
          _this.table_list = []
          _this.orderreleaseDataCancel()
          _this.getList()
          this.$q.loading.hide()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Release DN Code',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    orderreleaseDataCancel () {
      var _this = this
      _this.orderreleaseForm = false
      _this.orderreleaseid = 0
    },
    getFocus (number) {
      this.listNumber = number
    },
    setOptions (val) {
      const _this = this
      if (!val) {
        _this[`goodsData${_this.listNumber}`].code = ''
      }
      const needle = val.toLowerCase()
      getauth('goods/?goods_code__icontains=' + needle).then((res) => {
        const goodscodelist = []
        for (let i = 0; i < res.results.length; i++) {
          goodscodelist.push(res.results[i].goods_code)
          if (_this.listNumber) {
            if (res.results[i].goods_code === val) {
              _this[`goodsData${_this.listNumber}`].code = val
            }
          }
        }
        _this.options1 = goodscodelist
      })
    },
    filterFn (val, update, abort) {
      if (val.length < 1) {
        abort()
        return
      }
      update(() => {
        this.options = this.options1
      })
    },
    setModel (val) {
      const _this = this
      _this.newFormData.customer = val
    },
    filterFnS (val, update, abort) {
      var _this = this
      update(() => {
        const needle = val.toLocaleLowerCase()
        const data_filter = _this.customer_list1
        _this.customer_list = data_filter.filter(
          (v) => v.toLocaleLowerCase().indexOf(needle) > -1
        )
      })
    },
    PrintPickingList (e) {
      var _this = this
      var QRCode = require('qrcode')
      QRCode.toDataURL(e.bar_code, [
        {
          errorCorrectionLevel: 'H',
          mode: 'byte',
          version: '2',
          type: 'image/jpeg'
        }
      ])
        .then((url) => {
          _this.bar_code = url
        })
        .catch((err) => {
          console.error(err)
        })
      _this.viewPLForm = true
      getauth(_this.pathname + 'pickinglist/' + e.id + '/' + '?max_page=10000')
        .then((res) => {
          _this.pickinglist_print_table = []
          _this.picklist_check = 0
          res.forEach((item) => {
            if (item.picked_qty > 0) {
              _this.picklist_check += 1
            } else {
            }
          })
          _this.pickinglist_print_table = res
          _this.viewPLForm = true
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    pickedData (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.pickstock')) {
        _this.$q.notify({
          message:
            e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.pickstock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.pickFormData.dn_code = e.dn_code
        _this.pickFormData.customer = e.customer
        getauth(_this.pathname + 'pickinglist/' + e.id + '/').then((res) => {
          _this.pickedForm = true
          _this.pickedid = e.id
          _this.pickFormData.goodsData = res
        })
      }
    },
    pickedDataSubmit () {
      var _this = this
      // this.$q.loading.show({ message: '发货确认中' })
      this.$q.loading.show({ message: this.$t('twoKai.confirmingshipment') })
      _this.pickFormData.creater = _this.login_name
      postauth(
        _this.pathname + 'picked/' + _this.pickedid + '/',
        _this.pickFormData
      )
        .then((res) => {
          _this.table_list = []
          _this.pickedDataCancel()
          _this.getList()
          this.$q.loading.hide()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Confirm Picking List',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    pickedDataCancel () {
      var _this = this
      _this.pickedForm = false
      _this.pickedid = 0
      _this.pickFormData = {
        dn_code: '',
        customer: '',
        goodsData: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    viewData (e) {
      var _this = this
      ViewPrintAuth(_this.pathname + 'viewprint/' + e.id + '/').then((res) => {
        _this.viewprint_table = res.dn_detail
        _this.warehouse_detail = res.warehouse_detail
        _this.customer_detail = res.customer_detail
        _this.viewdn = e.dn_code
        var QRCode = require('qrcode')
        QRCode.toDataURL(e.bar_code, [
          {
            errorCorrectionLevel: 'H',
            mode: 'byte',
            version: '2',
            type: 'image/jpeg'
          }
        ])
          .then((url) => {
            _this.bar_code = url
          })
          .catch((err) => {
            console.error(err)
          })
        _this.viewForm = true
      })
    },
    filterFnDispatch (val, update, abort) {
      var _this = this
      if (val.length < 1) {
        abort()
        return
      }
      update(() => {
        const needle = val.toLowerCase()
        getauth('driver/?driver_name__icontains=' + needle)
          .then((res) => {
            const drivernamelist = []
            for (let i = 0; i < res.results.length; i++) {
              drivernamelist.push(res.results[i].driver_name)
            }
            LocalStorage.set('driver_name_list', drivernamelist)
            _this.driver_options = LocalStorage.getItem('driver_name_list')
            _this.$forceUpdate()
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      })
    },
    DispatchDN (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.pickedstock')) {
        _this.$q.notify({
          message:
            e.dn_code + ' DN Status Is Not ' + _this.$t('outbound.pickedstock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.dispatchFormData.dn_code = e.dn_code
        _this.dispatchid = e.id
        _this.dispatchForm = true
      }
    },
    dispatchDataCancel () {
      var _this = this
      _this.dispatchFormData = { dn_code: '', driver: '' }
      _this.dispatchForm = false
    },
    dispatchDataSubmit () {
      var _this = this
      // this.$q.loading.show({ message: '发车确认中' })
      this.$q.loading.show({ message: this.$t('twoKai.confirmationinprogress') })
      postauth(
        _this.pathname + 'dispatch/' + _this.dispatchid + '/',
        _this.dispatchFormData
      )
        .then((res) => {
          _this.table_list = []
          _this.dispatchDataCancel()
          _this.getList()
          this.$q.loading.hide()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Dispatch',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    PODData (e) {
      var _this = this
      if (e.dn_status !== _this.$t('outbound.shippedstock')) {
        _this.$q.notify({
          message:
            e.dn_code +
            ' DN Status Is Not ' +
            _this.$t('outbound.shippedstock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.podFormData.dn_code = e.dn_code
        _this.podFormData.customer = e.customer
        getauth(_this.pathname + 'detail/?dn_code=' + e.dn_code).then((res) => {
          _this.podForm = true
          _this.podid = e.id
          _this.podFormData.goodsData = res.results
        })
      }
    },
    PODDataCancel () {
      var _this = this
      _this.podForm = false
      _this.podid = 0
      _this.podFormData = {
        dn_code: '',
        customer: '',
        goodsData: []
      }
    },
    PODDataSubmit () {
      var _this = this
      if (!(_this.isError1 || _this.isError2)) {
        postauth(_this.pathname + 'pod/' + _this.podid + '/', _this.podFormData)
          .then((res) => {
            _this.table_list = []
            _this.PODDataCancel()
            _this.getList()
            if (!res.detail) {
              _this.$q.notify({
                message: 'Success Dispatch',
                icon: 'check',
                color: 'green'
              })
            }
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      }
    },
    BatchConfirmorderClick () {
      this.neworderidList = this.selected.filter(res => {
        return res.dn_status === this.$t('outbound.freshorder')
      })
      this.neworderListForm = true
    },
    neworderListDataSubmit () {
      var _this = this
      var PromiseAll = []
      this.neworderidList.map(neworderData => {
        PromiseAll.push(postauth(_this.pathname + 'neworder/' + neworderData.id + '/', {}))
      })
      Promise.all(PromiseAll).then((res) => {
        _this.table_list = []
        _this.neworderLisyDataCancel()
        _this.getList()
        if (!res.detail) {
          _this.$q.notify({
            message: 'Success Confirm DN Delivery',
            icon: 'check',
            color: 'green'
          })
        }
      }).catch((err) => {
        _this.neworderLisyDataCancel()
        _this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    },
    openPdf (e) {
      // this.viewForm = true
      this.src = baseurl + 'media/miandan/' + e + '.pdf'
      openURL(this.src)
    },
    getLocation (source) {
      let url = baseurl
      url += source
      console.log(url)
      return url
    }
  },
  created () {
    var _this = this
    if (LocalStorage.has('openid')) {
      _this.openid = LocalStorage.getItem('openid')
    } else {
      _this.openid = ''
      LocalStorage.set('openid', '')
    }
    if (LocalStorage.has('login_name')) {
      _this.login_name = LocalStorage.getItem('login_name')
    } else {
      _this.login_name = ''
      LocalStorage.set('login_name', '')
    }
    if (LocalStorage.has('auth')) {
      _this.authin = '1'
      _this.table_list = []
      _this.getList()
    } else {
      _this.authin = '0'
    }
    if (LocalStorage.has('goods_code_list')) {
    } else {
      LocalStorage.set('goods_code_list', [])
    }
  },
  mounted () {
    var _this = this
    if (_this.$q.platform.is.electron) {
      _this.height = String(_this.$q.screen.height - 290) + 'px'
    } else {
      _this.height = _this.$q.screen.height - 290 + '' + 'px'
    }
  },
  watch: {
    max_page_data (max_page_data) {
      var _this = this
      _this.getList()
    }
  },
  updated () {
  },
  destroyed () {
  }
}
</script>

<style lang="scss">
.custom-uploader {
  width: 100%;
  height: 80px;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  box-shadow: none;
  background: transparent !important;

  .q-uploader__header {
    height: 100%;
    background: transparent !important;
    color: #000;
    text-align: center;

    .q-btn {
      width: 100%;
      height: 100%;
    }

    .q-btn--round {
      border-radius: 0 !important;
    }
  }

  .q-uploader__list {
    display: none;
  }
}

.custom-download {
  margin-top: 20px;

  span {
    font-size: 14px;
    color: #000;
    cursor: pointer;
  }
}
</style>
