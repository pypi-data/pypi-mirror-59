#pragma once

#include <filesystem>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <unordered_map>

namespace ts {

using Path = std::filesystem::path;

template <class Base>
struct Factory {
    static std::unique_ptr<Base> make(std::string const& filename) {
        Path path{filename};
        auto it = data().find(path.extension().string());
        if (it == data().end())
            throw std::runtime_error{"Unsupported extension"};

        std::exception_ptr eptr;
        for (auto&& [prio, factory]: it->second)
            try {
                return factory(path);
            } catch (...) {
                eptr = std::current_exception();
            }
        if (eptr)
            std::rethrow_exception(eptr);
        return {};
    }

    template <class Derived>
    struct Register : Base {
        template <class... Ts>
        Register(Ts&&... args) : Base{std::forward<Ts>(args)...} {
            (void)is_registered;
        }

    private:
        static bool register_this() {
            static_assert(std::is_base_of_v<Register<Derived>, Derived>,
                          "Unregistered!!");
            for (const auto& ext : Derived::extensions) {
                auto& fc = Factory::data();
                if (!fc.contains(ext))
                    fc[ext] = {};
                fc[ext][Derived::priority] = &Derived::make_this;
            }
            return true;
        }

        inline static bool is_registered = register_this();
    };

private:
    friend Base;
    Factory() = default;

    static auto& data() {
        static std::unordered_map<
            std::string,
            std::map<int, std::unique_ptr<Base> (*)(const Path&)>>
            factories;
        return factories;
    }
};

} // namespace ts
