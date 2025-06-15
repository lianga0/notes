// https://github.com/lamerman/cpp-lru-cache
// 在 C++ 中，std::list 的 pop_back() 方法理论上是一个常数时间（O(1)）的操作，从尾部删除一个元素时，不需要遍历整个链表。
// 然而在 debug 模式下性能下降 的主要原因是与 调试工具和编译器内存检查机制 有关，而不是 pop_back() 方法本身的问题。

// debug 模式和 release 模式的区别
// debug 模式： 在 debug 模式下，标准库的容器可能进行额外的检查，确保程序的安全性。这些额外的检查可能包括：
// - 迭代器合法性检查：检查元素删除后是否存在残留无效迭代器。
// - 内存范围检查：针对链表节点，确认是否满足分配/释放要求，避免非法指针操作。
// - 额外的诊断代码：调试工具可能添加额外代码用于监控越界访问、未定义行为、动态内存问题等。
// release 模式： release 模式下这些检查部分被关闭，使代码运行更加轻量但没有额外保护，因此性能往往更高。
// 在 debug 模式下，容器操作的性能开销可能成倍增加，尤其是以链表等动态内存操作为主的容器。
// 
// std::list 特殊开销
// std::list 是双向链表，其每个节点存储了两个指针（前一个节点和后一个节点）。在 debug 模式下，针对操作的额外检查可能会显著增加开销。例如：
// - 内存分配/释放检查：每调用 pop_back()，都要释放最后一个节点并更新链表的末尾指针。在 debug 模式下，编译器可能逐步检查链表结构的内存一致性。
// - 迭代器失效检查：部分实现将对所有迭代器进行合法性验证，确认其失效处理是否正确。这会增加额外的计算开销。
// 这些额外的操作可能会使性能下降数百倍，尤其是在操作非常频繁的场景中，例如对列表的大量调用 pop_back()。

#include <list>
#include <unordered_map>
#include <memory>
#include <chrono>
#include <iostream>

#define MAX_SIZE	0x40

struct mm_cache_key {
	uint32_t process_id;
	uint32_t process_create_timestamp;
	unsigned char* scan_buff_address;
	uint32_t scan_buff_size;
	uint32_t scan_target_origin_size;
	uint32_t scan_target_frist_4bytes;

	bool operator==(const mm_cache_key& other) const {
		return process_id == other.process_id && process_create_timestamp == other.process_create_timestamp &&
			scan_buff_address == other.scan_buff_address && scan_buff_size == other.scan_buff_size &&
			scan_target_origin_size == other.scan_target_origin_size && scan_target_frist_4bytes == other.scan_target_frist_4bytes;
	}
};

namespace std {
	template <>
	struct hash<mm_cache_key> {
		size_t operator()(const mm_cache_key& key) const {
			size_t h1 = hash<uint32_t>{}(key.process_id);
			size_t h2 = hash<uint32_t>{}(key.process_create_timestamp);
			size_t h3 = hash<uintptr_t>{}(reinterpret_cast<uintptr_t>(key.scan_buff_address));
			size_t h4 = hash<uint32_t>{}(key.scan_buff_size);
			size_t h5 = hash<uint32_t>{}(key.scan_target_origin_size);
			size_t h6 = hash<uint32_t>{}(key.scan_target_frist_4bytes);
			return h1 ^ (h2 << 1) ^ (h3 >> 1) ^ h4 ^ (h5 << 2) ^ (h6 >> 2);
		}
	};
}
struct mm_detect_result {
	uint32_t detect_result;			
	char detect_name[MAX_SIZE + 1];
	uint64_t signature_id;	
};

typedef typename std::pair<mm_cache_key, mm_detect_result> key_value_pair_t;
typedef typename std::list<key_value_pair_t>::iterator list_iterator_t;

int main() {
	std::list<key_value_pair_t> cache_items_list;
	std::unordered_map<mm_cache_key, list_iterator_t> cache_items_map;
	int cache_size = 100000;
	for (int i = 0; i < cache_size * 2; i++) {
		mm_cache_key kk = { 0 };
		kk.process_id = i;
		mm_detect_result rr = { 0 };
		cache_items_list.push_front(key_value_pair_t(kk, rr));
		cache_items_map[kk] = cache_items_list.begin();
		if (i > cache_size) {
			std::cout << "Current cache list size:" << cache_items_list.size();
			auto start_time = std::chrono::high_resolution_clock::now(); // get performance start data
			cache_items_list.pop_back();
			auto end_time = std::chrono::high_resolution_clock::now(); // get performance end data
			std::chrono::duration<double, std::micro> elapsed_ms(end_time - start_time); // Calculate the time difference (in microseconds)
			std::cout << ", pop_back() cost:" << elapsed_ms.count() << " microseconds." << std::endl;
			start_time = std::chrono::high_resolution_clock::now(); // get performance start data
		}
	}
	return 0;
}
