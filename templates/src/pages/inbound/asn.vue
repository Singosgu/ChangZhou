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
      >
        <template v-slot:top>
          <q-btn-group push>
            <!-- <q-btn
              v-show="
                $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                $q.localStorage.getItem('staff_type') !== 'Customer' &&
                $q.localStorage.getItem('staff_type') !== 'Outbound' &&
                $q.localStorage.getItem('staff_type') !== 'StockControl'
              "
              :label="$t('new')"
              icon="add"
              @click="newFormOpen()"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
                >{{ $t("newtip") }}</q-tooltip
              >
            </q-btn> -->
            <q-btn
              v-show="
                $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                $q.localStorage.getItem('staff_type') !== 'Customer'
              "
              :label="$t('refresh')"
              icon="refresh"
              @click="reFresh()"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >{{ $t("refreshtip") }}
              </q-tooltip
              >
            </q-btn>
            <q-btn
              v-if="isVip9 === 9"
              @click="uploadVisible = true"
              :label="$t('upload_center.upload')"
              icon="file_upload"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >
                {{ $t("upload_center.uploadfiles") }}
              </q-tooltip>
            </q-btn>

            <!--  <q-btn
              @click="handleDownload"
              :label="$t('download')"
              icon="file_download"
            >
              <q-tooltip
                content-class="bg-amber text-black shadow-4"
                :offset="[10, 10]"
                content-style="font-size: 12px"
              >
                {{ $t("downloadtip") }}
              </q-tooltip>
            </q-btn> -->
          </q-btn-group>
          <q-space/>
          <q-input
            outlined
            rounded
            dense
            debounce="300"
            color="primary"
            v-model="filter"
            :placeholder="$t('search')"
            @blur="getSearchList()"
            @keyup.enter="getSearchList()"
          >
            <template v-slot:append>
              <q-icon name="search" @click="getSearchList()"/>
            </template>
          </q-input>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="asn_code" :props="props">{{ props.row.asn_code }}</q-td>
            <q-td key="asn_status" :props="props">{{
              props.row.asn_status
              }}
            </q-td>
            <q-td key="patch_number" :props="props">{{
              props.row.patch_number
              }}
            </q-td>
            <q-td key="warehouse_id" :props="props">
              {{ switchWarehouse(props.row) }}
            </q-td
            >
            <q-td key="total_weight" :props="props">{{
              props.row.total_weight.toFixed(4)
              }}
            </q-td>
            <q-td key="total_volume" :props="props">{{
              props.row.total_volume.toFixed(4)
              }}
            </q-td>
            <q-td key="total_quantity" :props="props">{{ props.row.total_quantity }}</q-td>
            <q-td key="box_number" :props="props">{{ props.row.box_number }}</q-td>
            <q-td key="confirm_time" :props="props">{{ props.row.confirm_time }}</q-td>

            <q-td key="creater" :props="props">{{ props.row.creater }}</q-td>
            <q-td key="create_time" :props="props">{{
              props.row.create_time
              }}
            </q-td>
            <q-td key="update_time" :props="props">{{
              props.row.update_time
              }}
            </q-td>
            <q-td key="action" :props="props" style="width: 100px">
              <q-btn
                v-show="
                  $q.localStorage.getItem('is_vip') === 9
                "
                round
                flat
                push
                color="info"
                icon="move_up"
                @click="ChangeWarehouse(props.row)"
              >
                <q-tooltip
                  content-class="bg-amber text-black shadow-4"
                  :offset="[10, 10]"
                  content-style="font-size: 12px"
                >调拨
                </q-tooltip
                >
              </q-btn>
              <q-btn
                v-show="
                  $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                  $q.localStorage.getItem('staff_type') !== 'Customer' &&
                  $q.localStorage.getItem('staff_type') !== 'Outbound' &&
                  $q.localStorage.getItem('staff_type') !== 'StockControl'
                "
                round
                flat
                push
                color="info"
                icon="visibility"
                @click="viewData(props.row)"
              >
                <q-tooltip
                  content-class="bg-amber text-black shadow-4"
                  :offset="[10, 10]"
                  content-style="font-size: 12px"
                >{{ $t("printthisasn") }}
                </q-tooltip
                >
              </q-btn>
              <q-btn
                v-show="
                  $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                  $q.localStorage.getItem('staff_type') !== 'Customer' &&
                  $q.localStorage.getItem('staff_type') !== 'Outbound' &&
                  $q.localStorage.getItem('staff_type') !== 'StockControl'
                "
                round
                flat
                push
                color="positive"
                icon="img:statics/inbound/preloadstock.png"
                @click="preloadData(props.row)"
              >
                <q-tooltip
                  content-class="bg-amber text-black shadow-4"
                  :offset="[10, 10]"
                  content-style="font-size: 12px"
                >{{ $t("confirmdelivery") }}
                </q-tooltip
                >
              </q-btn>
              <q-btn
                round
                flat
                push
                color="secondary"
                icon="file_download"
                @click="pdfDataForm(props.row)"
              >
                <q-tooltip
                  content-class="bg-amber text-black shadow-4"
                  :offset="[10, 10]"
                  content-style="font-size: 12px"
                >{{ $t("twoKai.download_tags") }}
                </q-tooltip
                >
              </q-btn>
              <q-btn
                v-show="
                  $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                  $q.localStorage.getItem('staff_type') !== 'Customer' &&
                  $q.localStorage.getItem('staff_type') !== 'Outbound' &&
                  $q.localStorage.getItem('staff_type') !== 'StockControl'
                "
                round
                flat
                push
                color="positive"
                icon="img:statics/inbound/presortstock.png"
                @click="presortData(props.row)"
              >
                <q-tooltip
                  content-class="bg-amber text-black shadow-4"
                  :offset="[10, 10]"
                  content-style="font-size: 12px"
                >{{ $t("finishloading") }}
                </q-tooltip
                >
              </q-btn>
              <q-btn
                v-show="
                  $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                  $q.localStorage.getItem('staff_type') !== 'Customer' &&
                  $q.localStorage.getItem('staff_type') !== 'Outbound' &&
                  $q.localStorage.getItem('staff_type') !== 'StockControl'
                "
                round
                flat
                push
                color="purple"
                icon="img:statics/inbound/sortstock.png"
                @click="sortedData(props.row)"
              >
                <q-tooltip
                  content-class="bg-amber text-black shadow-4"
                  :offset="[10, 10]"
                  content-style="font-size: 12px"
                >{{ $t("confirmsorted") }}
                </q-tooltip
                >
              </q-btn>
              <!-- <q-btn
                v-show="
                  $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                  $q.localStorage.getItem('staff_type') !== 'Customer' &&
                  $q.localStorage.getItem('staff_type') !== 'Outbound' &&
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
                  >{{ $t("edit") }}</q-tooltip
                >
              </q-btn> -->
              <q-btn
                v-show="
                  $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                  $q.localStorage.getItem('staff_type') !== 'Customer' &&
                  $q.localStorage.getItem('staff_type') !== 'Outbound' &&
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
          </q-tr>
        </template>
      </q-table>
    </transition>
    <template>
      <div class="q-pa-lg flex flex-center">
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
          :max="Math.ceil(page_count / 30 ) "
          :max-pages="30"
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
          <div>{{ newFormData.asn_code }}</div>
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
            v-model="newFormData.supplier"
            :options="supplier_list"
            @filter="filterFnS"
            @input-value="setModel"
            :label="$t('baseinfo.view_supplier.supplier_name')"
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

          <q-input
            dense
            outlined
            square
            v-model="newFormData.patch_number"
            :label="$t('twoKai.view_batch.batch_name')"
            :rules="[
              (val) =>
                (val && val.length > 0) || $t('twoKai.view_batch.error1'),
            ]"
          />

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
                ref="one"
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
    <q-dialog v-model="pdfForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>下载PDF</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
              $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-input dense
                   outlined
                   square
                   v-model="brand"
                   label="品牌"
                   autofocus
                   @keyup.enter="handleRecordDownload()"/>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="pdfDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn
            color="primary"
            @click="handleRecordDownload()"
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
    <q-dialog v-model="preloadForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ $t("confirmdelivery") }}</div>
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
          <q-input
            outlined
            v-model="deliveryData.box_number"
            :hint="$t('deliveryData.box_number')"
            :placeholder="$t('deliveryData.box_number_placeholder')"
          />
          <br>
          <q-input
            outlined
            v-model="deliveryData.confirm_time"
            mask="date"
            type="date"
            :hint="$t('deliveryData.confirm_time')"
            :placeholder="$t('deliveryData.confirm_time_placeholder')"
          >
          </q-input>
        </q-card-section
        >
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="preloadDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="preloadDataSubmit()">{{
            $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="presortForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ $t("finishloading") }}</div>
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
            @click="presortDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="presortDataSubmit()">{{
            $t("submit")
            }}
          </q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="viewForm">
      <div style="min-width: 1500px">
        <q-card id="printMe">
          <q-bar
            class="bg-light-blue-10 text-white rounded-borders"
            style="height: 50px"
          >
            <div>{{ viewAsn }}</div>
            <q-space/>
            {{ $t("inbound.asn") }}
          </q-bar>
          <q-card-section>
            <div class="row">
              <div class="col-8">
                <div class="text-h6">
                  Sender: {{ supplier_detail.supplier_name }}
                </div>
                <div class="text-subtitle2">
                  Address: {{ supplier_detail.supplier_city
                  }}{{ supplier_detail.supplier_address }}
                </div>
                <div class="text-subtitle2">
                  Tel: {{ supplier_detail.supplier_contact }}
                </div>
                <div class="text-h6">
                  Receiver: {{ warehouse_detail.warehouse_name }}
                </div>
                <div class="text-subtitle2">
                  Address: {{ warehouse_detail.warehouse_city
                  }}{{ warehouse_detail.warehouse_address }}
                </div>
                <div class="text-subtitle2">
                  Tel: {{ warehouse_detail.warehouse_contact }}
                </div>
              </div>
              <div class="col-4">
                <img :src="bar_code" style="width: 70%; margin-left: 15%"/>
              </div>
            </div>
          </q-card-section>
          <q-markup-table>
            <thead>
            <tr>
              <th class="text-left">
                {{ $t("goods.view_goodslist.goods_code") }}
              </th>
              <th class="text-right">
                {{ $t("stock.view_stocklist.goods_qty") }}
              </th>
              <th class="text-center">
                {{ $t("twoKai.warehouse_id") }}
              </th>
              <th class="text-right">
                {{ $t("inbound.view_asn.total_weight") }}
              </th>
              <th class="text-right">
                {{ $t("inbound.view_asn.total_volume") }}
              </th>
              <th class="text-right">
                {{ $t("inbound.view_asn.goods_actual_qty") }}
              </th>
              <th class="text-right">Comments</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(view, index) in viewprint_table" :key="index">
              <td class="text-left">{{ view.goods_code }}</td>
              <td class="text-right">{{ view.goods_qty }}</td>
              <td class="text-right">
                {{ switchWarehouse(view) }}
              </td>
              <td class="text-right">{{ view.goods_weight }}</td>
              <td class="text-right">{{ view.goods_volume }}</td>
              <td class="text-right">{{ view.goods_actual_qty }}</td>
              <td class="text-right"></td>
            </tr>
            </tbody>
          </q-markup-table>
        </q-card>
      </div>
      <div style="float: right; padding: 15px 15px 15px 0">
        <q-btn color="primary" icon="print" v-print="printObj">print</q-btn>
      </div>
    </q-dialog>
    <q-dialog v-model="sortedForm">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>{{ sorted_list.asn_code }}</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
              $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-select outlined v-model="sorted_list.bin_name" :options="bin_list_detail" label="缓存区"/>
          <q-input
            dense
            outlined
            square
            debounce="500"
            disable
            readonly
            v-model="sorted_list.supplier"
            :label="$t('baseinfo.view_supplier.supplier_name')"
            style="margin-bottom: 5px"
          />
          <div v-for="(item, index) in sorted_list.goodsData" :key="index">
            <q-input
              dense
              outlined
              square
              bottom-slots
              type="number"
              v-model="item.goods_actual_qty"
              :label="$t('inbound.view_asn.goods_actual_qty')"
            >
              <template v-slot:append>
                {{ item.goods_code }}
              </template>
            </q-input>
          </div>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn
            color="white"
            text-color="black"
            style="margin-right: 25px"
            @click="sortedDataCancel()"
          >{{ $t("cancel") }}
          </q-btn
          >
          <q-btn color="primary" @click="sortedDataSubmit()">{{
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
    <q-dialog v-model="warehouse_form">
      <q-card class="shadow-24">
        <q-bar
          class="bg-light-blue-10 text-white rounded-borders"
          style="height: 50px"
        >
          <div>调拨</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{
              $t("index.close")
              }}
            </q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-select filled v-model="warehouse_model" :options="warehouse_options" label="仓库ID"/>
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
            @click="submitWarehouseChange()"
          >{{ $t("submit") }}
          </q-btn
          >
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>
<router-view/>

<script>
import {
  getauth,
  postauth,
  putauth,
  deleteauth,
  ViewPrintAuth,
  getfile,
  getpdfFile
} from 'boot/axios_request'

import {
  date,
  exportFile,
  SessionStorage,
  LocalStorage,
  openURL
} from 'quasar'

export default {
  name: 'Pageasnlist',
  data () {
    return {
      current: 1,
      page_count: 0,
      uploadVisible: false,
      token: LocalStorage.getItem('openid'),
      lang: LocalStorage.getItem('lang'),
      login_id: LocalStorage.getItem('login_id'),
      isVip9: LocalStorage.getItem('is_vip') || '',
      goodslistfile_pathname: baseurl + 'uploadfile/asnlistfileadd/',
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'asn/',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',
      brand: 'MADE IN CHINA',
      table_list: [],
      viewprint_table: [],
      bar_code: '',
      warehouse_detail: {},
      supplier_list: [],
      supplier_list1: [],
      deliveryData: {
        box_number: '',
        confirm_time: ''
      },
      supplier_detail: {},
      columns: [
        {
          name: 'asn_code',
          required: true,
          label: this.$t('inbound.view_asn.asn_code'),
          align: 'left',
          field: 'asn_code'
        },
        {
          name: 'asn_status',
          label: this.$t('inbound.view_asn.asn_status'),
          field: 'asn_status',
          align: 'center'
        },
        {
          name: 'patch_number',
          label: this.$t('twoKai.patch_number'),
          field: 'patch_number',
          align: 'center'
        },
        {
          name: 'warehouse_id',
          label: this.$t('twoKai.warehouse_id'),
          field: 'warehouse_id',
          align: 'center'
        },
        {
          name: 'total_weight',
          label: this.$t('inbound.view_asn.total_weight'),
          field: 'total_weight',
          align: 'center'
        },
        {
          name: 'total_volume',
          label: this.$t('inbound.view_asn.total_volume'),
          field: 'total_volume',
          align: 'center'
        },
        {
          name: 'total_quantity',
          label: this.$t('baseinfo.view_supplier.total_quantity'),
          field: 'total_quantity',
          align: 'center'
        },
        {
          name: 'box_number',
          label: this.$t('deliveryData.box_number'),
          field: 'box_number',
          align: 'center'
        },
        {
          name: 'confirm_time',
          label: this.$t('deliveryData.confirm_time'),
          field: 'confirm_time',
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
        rowsPerPage: '30'
      },
      newForm: false,
      options: SessionStorage.getItem('goods_code'),
      options1: [],
      isEdit: false,
      listNumber: '',
      newAsn: { creater: '' },
      warehouseId: '',
      newFormData: {
        asn_code: '',
        patch_number: '',
        supplier: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      },
      goodsData1: { code: '', qty: '' },
      goodsData2: { code: '', qty: '' },
      goodsData3: { code: '', qty: '' },
      goodsData4: { code: '', qty: '' },
      goodsData5: { code: '', qty: '' },
      goodsData6: { code: '', qty: '' },
      goodsData7: { code: '', qty: '' },
      goodsData8: { code: '', qty: '' },
      goodsData9: { code: '', qty: '' },
      goodsData10: { code: '', qty: '' },
      editid: 0,
      editFormData: {},
      pdfData: {},
      sortedForm: false,
      sortedid: 0,
      sorted_list: {
        bin_name: '',
        asn_code: '',
        supplier: '',
        goodsData: [],
        creater: ''
      },
      deleteForm: false,
      pdfForm: false,
      deleteid: 0,
      preloadForm: false,
      preloadid: 0,
      presortForm: false,
      presortid: 0,
      viewForm: false,
      viewAsn: '',
      viewid: 0,
      printObj: {
        id: 'printMe',
        popTitle: this.$t('inbound.asn')
      },
      devi: window.device,
      error1: this.$t('baseinfo.view_supplier.error1'),
      goodsListData: [],
      warehouse_list: [1, 2, 3, 4, 5, 6, 7],
      warehouse_form: false,
      warehouse_model: null,
      warehouse_options: [],
      asn_choose_data: null,
      bin_list_detail: [],
      bin_list: []
    }
  },
  methods: {
    handleRecordDownload () {
      if (LocalStorage.has('auth')) {
        getpdfFile(
            `asn/pdfdownload/${this.pdfData.id}/?lang=${LocalStorage.getItem('lang')}&brand=${this.brand}`
        ).then((res) => {
          var timeStamp = Date.now()
          var formattedString = date.formatDate(timeStamp, 'YYYYMMDDHHmmssSSS')
          const status = exportFile(
              `asn_filedetail_${this.pdfData.id}_${formattedString}.pdf`,
              res.data,
              'application/pdf'
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
    handleDownload () {
      const _this = this
      getfile(
        _this.pathname + 'filelist/?lang=' + LocalStorage.getItem('lang')
      ).then((res) => {
        var timeStamp = Date.now()
        var formattedString = date.formatDate(timeStamp, 'YYYYMMDDHHmmssSSS')
        const status = exportFile(
          _this.pathname + formattedString + '.csv',
          '\uFEFF' + res.data,
          'text/csv'
        )
        if (status !== true) {
          _this.$q.notify({
            message: 'Browser denied file download...',
            color: 'negative',
            icon: 'warning'
          })
        }
      })
    },
    onRejected (rejectedEntries) {
      this.$q.notify({
        type: 'negative',
        message: `${rejectedEntries.length} file(s) did not pass validation constraints`
      })
    },
    getfileinfo (file) {
      console.log(file, '------')
    },
    handleUploadFinish () {
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
            openURL(baseurl + 'media/upload_example/asnlist_cn.xlsx')
          } else {
            openURL(baseurl + 'media/upload_example/asnlist_en.xlsx')
          }
        } else {
          openURL(baseurl + 'media/upload_example/asnlist_en.xlsx')
        }
      } else {
        _this.$q.notify({
          message: _this.$t('notice.loginerror'),
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
    getList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname + 'list/' + '?page=' + this.current, {})
          .then((res) => {
            _this.page_count = res.count
            _this.table_list = []
            res.results.forEach((item) => {
              if (item.asn_status === 1) {
                item.asn_status = _this.$t('inbound.predeliverystock')
              } else if (item.asn_status === 2) {
                item.asn_status = _this.$t('inbound.preloadstock')
              } else if (item.asn_status === 3) {
                item.asn_status = _this.$t('inbound.presortstock')
              } else if (item.asn_status === 4) {
                item.asn_status = _this.$t('inbound.sortstock')
              } else if (item.asn_status === 5) {
                item.asn_status = _this.$t('inbound.asndone')
              } else {
                item.asn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.supplier_list = res.supplier_list
            _this.supplier_list1 = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
            _this.goodsListData = res.results
            _this.warehouse_list = res.warehouse_list
            _this.warehouse_options = res.warehouse_list
            _this.bin_list = res.bin_list
          })
          .catch((err) => {
            console.log(err)
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
        getauth(
          _this.pathname + 'list/?search=' + _this.filter + '&page=' + this.current,
          {}
        )
          .then((res) => {
            _this.page_count = res.count
            _this.table_list = []
            res.results.forEach((item) => {
              if (item.asn_status === 1) {
                item.asn_status = _this.$t('inbound.predeliverystock')
              } else if (item.asn_status === 2) {
                item.asn_status = _this.$t('inbound.preloadstock')
              } else if (item.asn_status === 3) {
                item.asn_status = _this.$t('inbound.presortstock')
              } else if (item.asn_status === 4) {
                item.asn_status = _this.$t('inbound.sortstock')
              } else if (item.asn_status === 5) {
                item.asn_status = _this.$t('inbound.asndone')
              } else {
                item.asn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.supplier_list = res.supplier_list
            _this.supplier_list1 = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
            _this.bin_list = res.bin_list
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
              if (item.asn_status === 1) {
                item.asn_status = _this.$t('inbound.predeliverystock')
              } else if (item.asn_status === 2) {
                item.asn_status = _this.$t('inbound.preloadstock')
              } else if (item.asn_status === 3) {
                item.asn_status = _this.$t('inbound.presortstock')
              } else if (item.asn_status === 4) {
                item.asn_status = _this.$t('inbound.sortstock')
              } else if (item.asn_status === 5) {
                item.asn_status = _this.$t('inbound.asndone')
              } else {
                item.asn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.supplier_list = res.supplier_list
            _this.supplier_list1 = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
            _this.bin_list = res.bin_list
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
              if (item.asn_status === 1) {
                item.asn_status = _this.$t('inbound.predeliverystock')
              } else if (item.asn_status === 2) {
                item.asn_status = _this.$t('inbound.preloadstock')
              } else if (item.asn_status === 3) {
                item.asn_status = _this.$t('inbound.presortstock')
              } else if (item.asn_status === 4) {
                item.asn_status = _this.$t('inbound.sortstock')
              } else if (item.asn_status === 5) {
                item.asn_status = _this.$t('inbound.asndone')
              } else {
                item.asn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.supplier_list = res.supplier_list
            _this.supplier_list1 = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
            _this.bin_list = res.bin_list
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
    pdfDataForm (e) {
      var _this = this
      _this.pdfData = e
      _this.pdfForm = true
    },
    pdfDataCancel () {
      var _this = this
      _this.brand = 'MADE IN CHINA'
      _this.pdfForm = false
    },
    newFormOpen () {
      var _this = this
      _this.isEdit = false
      _this.goodsDataClear()
      _this.newForm = true
      _this.newAsn.creater = _this.login_name
      postauth(_this.pathname + 'list/', _this.newAsn)
        .then((res) => {
          if (!res.detail) {
            _this.newFormData.asn_code = res.asn_code
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
      if (!_this.newFormData.patch_number) {
        _this.$q.notify({
          message: 'Please Enter The patch_number',
          icon: 'close',
          color: 'negative'
        })
        return
      }
      if (!_this.warehouseId) {
        _this.$q.notify({
          message: 'Please Enter The warehouse',
          icon: 'close',
          color: 'negative'
        })
        return
      }
      let cancelRequest = false
      if (_this.newFormData.supplier !== '') {
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
          message: 'Please Enter The Supplier',
          icon: 'close',
          color: 'negative'
        })
      }
      if (!cancelRequest) {
        postauth(_this.pathname + 'detail/', {
          ..._this.newFormData,
          page_size: 1000,
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
      _this.warehouseId = ''
      _this.newFormData = {
        asn_code: '',
        supplier: '',
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
    editData (e) {
      var _this = this
      _this.isEdit = true
      _this.goodsDataClear()
      if (e.asn_status !== _this.$t('inbound.predeliverystock')) {
        _this.$q.notify({
          message:
              e.asn_code +
              ' ASN Status Is Not ' +
              _this.$t('inbound.predeliverystock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.newFormData.asn_code = e.asn_code
        _this.newFormData.supplier = e.supplier
        _this.newFormData.patch_number = e.patch_number
        _this.warehouseId = e.warehouse_id
        getauth(_this.pathname + 'detail/?asn_code=' + e.asn_code).then(
          (res) => {
            _this.newForm = true
            _this.editid = e.id
            res.results.forEach((detail, index) => {
              _this[`goodsData${index + 1}`] = {
                code: detail.goods_code,
                qty: detail.goods_qty
              }
            })
          }
        )
      }
    },
    editDataSubmit () {
      var _this = this
      _this.newFormData.creater = _this.login_name
      let cancelRequest = false
      if (_this.newFormData.supplier !== '') {
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
          message: 'Please Enter The Supplier',
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
            if (res.detail === 'success') {
              _this.$q.notify({
                message: 'Success Edit Data',
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
        asn_code: '',
        supplier: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    deleteData (e) {
      var _this = this
      if (e.asn_status !== _this.$t('inbound.predeliverystock')) {
        _this.$q.notify({
          message:
              e.asn_code +
              ' ASN Status Is Not ' +
              _this.$t('inbound.predeliverystock'),
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
          if (!res.data) {
            _this.$q.notify({
              message: 'Success Delete Data',
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
    preloadData (e) {
      var _this = this
      if (e.asn_status !== _this.$t('inbound.predeliverystock')) {
        _this.$q.notify({
          message:
              e.asn_code +
              ' ASN Status Is Not ' +
              _this.$t('inbound.predeliverystock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.preloadForm = true
        _this.preloadid = e.id
      }
    },
    preloadDataSubmit () {
      var _this = this
      if (!this.deliveryData.box_number) {
        _this.$q.notify({
          message: 'Carton Number Cannot be empty',
          icon: 'close',
          color: 'negative'
        })
        return
      }
      if (!this.deliveryData.confirm_time) {
        _this.$q.notify({
          message: 'Confirmation Time Cannot be empty',
          icon: 'close',
          color: 'negative'
        })
        return
      }

      postauth(_this.pathname + 'preload/' + _this.preloadid + '/', { ...this.deliveryData })
        .then((res) => {
          _this.table_list = []
          _this.preloadDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Confirm ASN Delivery',
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
    preloadDataCancel () {
      var _this = this
      _this.preloadForm = false
      _this.preloadid = 0
    },
    presortData (e) {
      var _this = this
      if (e.asn_status !== _this.$t('inbound.preloadstock')) {
        _this.$q.notify({
          message:
              e.asn_code +
              ' ASN Status Is Not ' +
              _this.$t('inbound.preloadstock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.presortForm = true
        _this.presortid = e.id
      }
    },
    presortDataSubmit () {
      var _this = this
      postauth(_this.pathname + 'presort/' + _this.presortid + '/', {})
        .then((res) => {
          _this.table_list = []
          _this.presortDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Load ASN',
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
    presortDataCancel () {
      var _this = this
      _this.presortForm = false
      _this.presortid = 0
    },
    getFocus (number) {
      this.listNumber = number
    },
    setOptions (val) {
      const _this = this
      if (!val) {
        this[`goodsData${this.listNumber}`].code = ''
      }
      const needle = val.toLowerCase()
      getauth('goods/?goods_code__icontains=' + needle).then((res) => {
        const goodscodelist = []
        for (let i = 0; i < res.results.length; i++) {
          goodscodelist.push(res.results[i].goods_code)
          if (this.listNumber) {
            if (res.results[i].goods_code === val) {
              this[`goodsData${this.listNumber}`].code = val
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

      _this.newFormData.supplier = val
    },
    setWarehouse (val) {
      const _this = this
      console.log(val, '====211====')
      this.$nextTick(() => {
        _this.aaa = val
        console.log(val, '====211====')
      })
    },
    filterFnS (val, update, abort) {
      var _this = this
      update(() => {
        const needle = val.toLocaleLowerCase()
        const data_filter = _this.supplier_list1
        _this.supplier_list = data_filter.filter(
          (v) => v.toLocaleLowerCase().indexOf(needle) > -1
        )
      })
    },
    sortedData (e) {
      var _this = this
      _this.goodsDataClear()
      if (e.asn_status !== _this.$t('inbound.presortstock')) {
        _this.$q.notify({
          message:
              e.asn_code +
              ' ASN Status Is Not ' +
              _this.$t('inbound.presortstock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.bin_list.forEach(item => {
          if (item.openid === e.openid) {
          }
        })
        _this.sorted_list.asn_code = e.asn_code
        _this.sorted_list.supplier = e.supplier
        getauth(_this.pathname + 'detail/?max_page=10000&asn_code=' + e.asn_code).then(
          (res) => {
            _this.sortedForm = true
            _this.sortedid = e.id
            // TODO 这里会引起一个数据量为0的BUG
            _this.sorted_list.goodsData = res.results
            _this.sorted_list.goodsData.forEach(item => {
              item.goods_actual_qty = item.goods_qty
            })
          }
        )
      }
    },
    sortedDataSubmit () {
      var _this = this
      _this.sorted_list.creater = _this.login_name
      postauth(
        _this.pathname + 'sorted/' + _this.sortedid + '/',
        _this.sorted_list
      )
        .then((res) => {
          _this.table_list = []
          _this.sortedDataCancel()
          _this.getList()
          if (!res.data) {
            _this.$q.notify({
              message: 'Success Sorted ASN',
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
    sortedDataCancel () {
      var _this = this
      _this.sortedForm = false
      _this.sortedid = 0
      _this.sorted_list = {
        bin_name: '',
        asn_code: '',
        supplier: '',
        goodsData: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    viewData (e) {
      var _this = this
      ViewPrintAuth(_this.pathname + 'viewprint/' + e.id + '/').then((res) => {
        _this.viewprint_table = res.asn_detail
        _this.warehouse_detail = res.warehouse_detail
        _this.supplier_detail = res.supplier_detail
        _this.viewAsn = e.asn_code
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
    ChangeWarehouse (e) {
      var _this = this
      _this.warehouse_form = true
      _this.asn_choose_data = e
    },
    submitWarehouseChange () {
      var _this = this
      if (_this.warehouse_model.value === _this.asn_choose_data.warehouse_id) {
        _this.$q.notify({
          message: '同一个仓库不可以调拨',
          icon: 'close',
          color: 'negative'
        })
      } else {
        postauth(
          _this.pathname + 'changewarehouse/' + _this.asn_choose_data.id + '/',
          _this.warehouse_model
        )
          .then((res) => {
            _this.table_list = []
            _this.warehouse_form = false
            _this.getList()
            if (!res.data) {
              _this.$q.notify({
                message: '调拨成功',
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
    if (SessionStorage.has('goods_code')) {
    } else {
      SessionStorage.set('goods_code', [])
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
