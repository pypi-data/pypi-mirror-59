#pragma once

#include <memory>
#include <sstream>

#include <openslide/openslide.h>

#include "tensor.h"
#include "dispatch.h"

namespace ts::os {

// ------------------------------ declarations ------------------------------

struct File {
    File(Path const& path);
    inline operator openslide_t*() const noexcept { return _ptr.get(); }
    inline operator openslide_t*() noexcept { return _ptr.get(); }

private:
    std::unique_ptr<openslide_t, void (*)(openslide_t*)> _ptr;
};

struct OpenSlide final : Dispatch<OpenSlide> {
    static inline constexpr int priority = 1;
    static inline constexpr const char* extensions[] = {
        ".bif", ".ndpi", ".mrxs", ".scn", ".svs", ".svslide", ".tif", ".tiff", ".vms", ".vmu"};

    template <class... Ts>
    OpenSlide(File file, std::array<uint8_t, 3> bg_color, Ts&&... args) noexcept
      : Dispatch{std::forward<Ts>(args)...}
      , _file{std::move(file)}
      , _bg_color{std::move(bg_color)}
    {}

    static std::unique_ptr<Image> make_this(Path const& path);

    template <typename T>
    Tensor<T> read(Box const&) const {
        throw std::runtime_error{"Not implemented"};
    }

    template <>
    Tensor<uint8_t> read(Box const& box) const;

private:
    File _file;
    std::array<uint8_t, 3> _bg_color;

    // std::string get(std::string const& name) const;
    // void cache_capacity(size_t capacity);
};

// ------------------------ non-template definitions ------------------------

auto os_open(Path const& path) {
    auto c_path = path.string();
    if (!openslide_detect_vendor(c_path.c_str()))
        throw std::runtime_error{"Cant open without vendor"};

    auto ptr = openslide_open(c_path.c_str());
    if (const char* error = openslide_get_error(ptr))
        throw std::runtime_error{error};

    return ptr;
}

File::File(Path const& path) : _ptr{os_open(path), openslide_close} {}

std::unique_ptr<Image> OpenSlide::make_this(Path const& path) {
    auto file = File{path};
    auto levels_num = openslide_get_level_count(file);

    std::map<Level, LevelInfo> levels;
    for (Level level = 0; level < levels_num; ++level) {
        int64_t y;
        int64_t x;
        openslide_get_level_dimensions(file, level, &x, &y);

        std::string tag_h
            = "openslide.level[" + std::to_string(level) + "].tile-height";
        std::string tag_w
            = "openslide.level[" + std::to_string(level) + "].tile-width";
        auto lh = openslide_get_property_value(file, tag_h.c_str());
        auto lw = openslide_get_property_value(file, tag_w.c_str());

        levels[level] = {
            {static_cast<uint32_t>(y), static_cast<uint32_t>(x), 3},
            {std::stoi(lh, 0, 10), std::stoi(lw, 0, 10), 3}
        };
    }

    // std::vector<float> spacing;
    // for (auto tag: {OPENSLIDE_PROPERTY_NAME_MPP_Y, OPENSLIDE_PROPERTY_NAME_MPP_X}) {
    //     std::stringstream ssm{openslide_get_property_value(file, tag)};
    //     if (ssm) {
    //         float tmp;
    //         ssm >> tmp;
    //         spacing.push_back(tmp);
    //     }
    // }

    // Get background color if present
    std::array<uint8_t, 3> bg_color = {255, 255, 255};
    char const* bg_color_hex
        = openslide_get_property_value(file, "openslide.background-color");
    if (bg_color_hex) {
        uint32_t bg_color32 = std::stoi(bg_color_hex, 0, 16);
        bg_color[0] = 0xFF & (bg_color32 >> 16);  // R
        bg_color[1] = 0xFF & (bg_color32 >> 8);   // G
        bg_color[2] = 0xFF & bg_color32;          // B
    }

    return std::make_unique<OpenSlide>(
        std::move(file), std::move(bg_color), uint8_t{}, 3, std::move(levels)
    );
}

// We are using OpenSlides caching system instead of our own.
// void OpenSlide::cache_capacity(size_t capacity) {
// #ifdef CUSTOM_OPENSLIDE
//     if (slide_)
//         openslide_set_cache_size(slide_, capacity);
// #endif
// }

// std::string OpenSlide::get(const std::string& name) const {
//     std::string value;
//     if (value = openslide_get_property_value(file_, name.c_str()))
//         return value;
//     return {};
// }

template <>
Tensor<uint8_t> OpenSlide::read(Box const& box) const {
    Tensor<uint8_t> buf{{box.shape(0), box.shape(1), Size{4}}};
    openslide_read_region(
        _file, reinterpret_cast<uint32_t*>(buf.data()),
        box.min_[1], box.min_[0], box.level,
        box.shape(1), box.shape(0));

    Tensor<uint8_t> result{{box.shape(0), box.shape(1), Size{3}}};

    auto b = buf.template view<3>();
    auto r = result.template view<3>();

    for (Size y = 0; y < box.shape(0); ++y)
        for (Size x = 0; x < box.shape(1); ++x) {
            std::reverse_copy(&b({y, x}), &b({y, x, 3}), &r({y, x, 3}));
            // const auto alpha = r({y, x, 3});
            // if (alpha == 255) {
            //     r({y, x, 0}) = b({y, x, 2});
            //     r({y, x, 1}) = b({y, x, 1});
            //     r({y, x, 2}) = b({y, x, 0});
            // } else if (alpha == 0) {
            //     r({y, x, 0}) = _bg_color[0];
            //     r({y, x, 1}) = _bg_color[1];
            //     r({y, x, 2}) = _bg_color[2];
            // } else {
            //     r({y, x, 0}) = (255.f * b({y, x, 2})) / alpha;
            //     r({y, x, 1}) = (255.f * b({y, x, 1})) / alpha;
            //     r({y, x, 2}) = (255.f * b({y, x, 0})) / alpha;
            // }
        }
    return result;
}

} // namespace ts::os
